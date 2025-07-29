"""
TODO: custom otel span attributes
TODO: custom access logging extras
TODO: custome bg logging format
"""

import logging
import time
from contextlib import AbstractContextManager, ExitStack
from typing import Any, Literal, assert_never

from django.db import connections
from dramatiq import Broker, Message, Middleware
from opentelemetry import trace
from opentelemetry.propagate import extract, inject
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span, status

from ..django.middleware import _SqlCounterQueryWrapper

_DRAMATIQ_MESSAGE_TAG_KEY = "dramatiq.action"
_DRAMATIQ_MESSAGE_SEND = "send"
_DRAMATIQ_MESSAGE_RUN = "run"
_DRAMATIQ_MESSAGE_RETRY_COUNT_KEY = "dramatiq.retry_count"

logger = logging.getLogger(__name__)

BG_LOGGING_DATE_FORMAT = "YYYY-MM-DD HH:mm:ss"


def get_operation_name(
    hook_name: Literal["before_process_message", "before_enqueue"],
    actor_name: str,
    retry_count: int,
) -> str:
    """Generate an operation name"""
    match hook_name:
        case "before_process_message":
            return (
                f"dramatiq.process/{actor_name}"
                if retry_count == 0
                else f"dramatiq/process(retry-{retry_count})/{actor_name}"
            )
        case "before_enqueue":
            return (
                f"dramatiq.send/{actor_name}"
                if retry_count == 0
                else f"dramatiq/send(retry-{retry_count})/{actor_name}"
            )
        case unreachable:
            assert_never(unreachable)


class UptickSqlCounterDramatiqMiddleware(Middleware):
    """
    Middleware to count sql queries executed during a bgtask.

    Also injects a comment into the sql query with the controller name to help
    debug where a slow query is coming from.
    """

    def before_process_message(self, broker: Broker, message: Message) -> None:
        """Called before a message is processed."""
        controller = message.actor_name
        stack = ExitStack().__enter__()
        for db_alias in connections:
            stack.enter_context(
                connections[db_alias].execute_wrapper(
                    _SqlCounterQueryWrapper(message, controller=controller)
                )
            )
        message._sql_activation = stack  # type: ignore

    def after_process_message(
        self,
        broker: Broker,
        message: Message,
        *,
        result: Any = None,
        exception: Any = None,
    ) -> None:
        """Called after a message has been processed."""
        message._sql_activation.__exit__(None, None, None)  # type: ignore


class OTELMiddleware(Middleware):
    """This middleware adds opentelemetry instrumenting to dramatiq tasks.

    OTEL context is propagated via the message options dict before a messge is sent and
    used to create a span when a message is received.

    This is heavily based off opentelemetry-instrumentation-remoulade (a fork of dramatiq).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._tracer: trace.Tracer | None = None
        self.span_registry: dict[
            tuple[Any, bool], tuple[Span, AbstractContextManager[Span]]
        ] = {}
        super().__init__(*args, **kwargs)

    @property
    def tracer(self) -> trace.Tracer:
        """Get the tracer instance in a lazy fashion."""
        if not self._tracer:
            self._tracer = trace.get_tracer(
                instrumenting_module_name="dramatiq",
                instrumenting_library_version="0.1.0",
                schema_url="https://opentelemetry.io/schemas/1.11.0",
            )
        return self._tracer

    @classmethod
    def _get_message_attributes(
        self, message: Message, **kwargs: Any
    ) -> dict[str, Any]:
        return {
            "dramatiq.actor_name": message.actor_name,
            SpanAttributes.MESSAGING_MESSAGE_ID: message.message_id,
            **kwargs,
        }

    def before_process_message(self, broker: Broker, message: Message) -> None:
        if "trace_ctx" not in message.options:
            return

        trace_ctx = extract(message.options["trace_ctx"])
        retry_count = message.options.get("retries", 0)
        operation_name = get_operation_name(
            "before_process_message", message.actor_name, retry_count
        )
        span_attributes = {
            _DRAMATIQ_MESSAGE_RETRY_COUNT_KEY: retry_count,
        }

        span = self.tracer.start_span(
            operation_name,
            kind=trace.SpanKind.CONSUMER,
            context=trace_ctx,
            attributes=span_attributes,
        )

        activation = trace.use_span(span, end_on_exit=True)
        activation.__enter__()  # pylint: disable=E1101
        self.attach_span(message.message_id, (span, activation))

    def after_process_message(
        self,
        broker: Broker,
        message: Message,
        *,
        result: Any | None = None,
        exception: Exception | None = None,
    ) -> None:
        span, activation = self.retrieve_span(message.message_id)

        if span is None:
            # no existing span found for message_id
            return

        if span.is_recording():
            span.set_attributes(
                {
                    _DRAMATIQ_MESSAGE_TAG_KEY: _DRAMATIQ_MESSAGE_RUN,
                    "sql_count": getattr(message, "query_count", 0),
                    **self._get_message_attributes(message),
                }
            )
            if exception:
                span.record_exception(exception)
                span.set_status(status.Status(status.StatusCode.ERROR, str(exception)))
                span.set_attribute("error_count", 1)
            else:
                span.set_status(status.Status(status.StatusCode.OK))

        if activation:
            activation.__exit__(None, None, None)
        self.detach_span(message.message_id, is_publish=False)

    def before_enqueue(
        self,
        _broker: Broker,
        message: Message,
        delay: int,
        exception: Exception | None = None,
    ) -> None:
        retry_count = message.options.get("retries", 0)
        operation_name = get_operation_name(
            "before_enqueue", message.actor_name, retry_count
        )
        span_attributes = {_DRAMATIQ_MESSAGE_RETRY_COUNT_KEY: retry_count}

        span = self.tracer.start_span(
            operation_name,
            kind=trace.SpanKind.PRODUCER,
            attributes=span_attributes,
        )

        if span.is_recording():
            span.set_attributes(
                {
                    **self._get_message_attributes(message, delay=delay),
                    _DRAMATIQ_MESSAGE_TAG_KEY: _DRAMATIQ_MESSAGE_SEND,
                }
            )

        activation = trace.use_span(span, end_on_exit=True)
        activation.__enter__()

        self.attach_span(
            message.message_id,
            (span, activation),
            is_publish=True,
        )

        if "trace_ctx" not in message.options:
            message.options["trace_ctx"] = {}
        inject(message.options["trace_ctx"])

    def after_enqueue(self, broker: Broker, message: Message, delay: int) -> None:
        _, activation = self.retrieve_span(message.message_id, is_publish=True)

        if activation is None:
            # no existing span found for message_id
            return

        activation.__exit__(None, None, None)
        self.detach_span(message.message_id, is_publish=True)

    # Utilities
    def attach_span(
        self,
        message_id: Any,
        span_and_activation: tuple[Span, AbstractContextManager[Span]],
        is_publish: bool = False,
    ) -> None:
        self.span_registry[(message_id, is_publish)] = span_and_activation

    def detach_span(self, message_id: Any, is_publish: bool = False) -> None:
        self.span_registry.pop((message_id, is_publish))

    def retrieve_span(
        self, message_id: Any, is_publish: bool = False
    ) -> tuple[Span | None, AbstractContextManager[Span] | None]:
        return self.span_registry.get((message_id, is_publish), (None, None))


class MessageLoggingMiddleware(Middleware):
    """This middleware adds additional logging"""

    BG_LOGGING_FORMAT = "{pre_message} {actor} {message_id} {user_id}  {duration}"

    def before_process_message(self, broker: Broker, message: Any) -> None:
        """Sets up USER context"""
        message.started = time.time()  # t
        message._user = message.options.get("user", {})

        logger.info(
            self.BG_LOGGING_FORMAT.format(
                pre_message="Beginning Task:",
                actor=message.actor_name,
                user_id=(
                    f"user_id={message._user.get('id', '')}" if message._user else ""
                ),
                message_id=message.message_id,
                duration="",
            )
        )

    def after_process_message(
        self,
        broker: Broker,
        message: Any,
        *,
        result: Any = None,
        exception: Any = None,
    ) -> None:
        duration = time.time() - message.started
        logger.info(
            self.BG_LOGGING_FORMAT.format(
                pre_message="Finishing Task:",
                actor=message.actor_name,
                user_id=(
                    f"user_id={message._user.get('id', '')}" if message._user else ""
                ),
                message_id="message_id=" + message.message_id,
                duration=f"duration={duration:0.3f}s",
            )
        )
