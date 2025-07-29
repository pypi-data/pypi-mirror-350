import logging
import os
from collections.abc import Callable
from typing import Any

from opentelemetry._logs import set_logger_provider
from opentelemetry._logs._internal import ProxyLoggerProvider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs._internal import (
    LoggingHandler,
    get_logger,
    get_logger_provider,
)
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
    LogExporter,
)
from opentelemetry.sdk.trace import Span


def manually_instrument_logging(
    log_hook: Callable[[Span, logging.LogRecord], None] | None = None,
    default_django_config: bool = True,
) -> None:
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    if os.environ.get("OTEL_SDK_DISABLED"):
        return

    if not isinstance(get_logger_provider(), ProxyLoggerProvider):
        return

    # Configure the logging provider
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    if logs_exporter_envar := os.environ.get("OTEL_LOGS_EXPORTER"):
        log_exporter: LogExporter
        if logs_exporter_envar == "otlp":
            log_exporter = OTLPLogExporter()
        else:
            log_exporter = ConsoleLogExporter()
        batch_log_processor = BatchLogRecordProcessor(log_exporter)
        logger_provider.add_log_record_processor(batch_log_processor)

    LoggingInstrumentor().instrument(log_hook=log_hook)

    try:
        if default_django_config:
            from django.conf import settings  # type: ignore

            settings["LOGGING"] = DEFAULT_LOGGING_CONFIG_DICT
    except Exception:
        pass


# This is a predefined simple logging config that can be simply imported into djangos base settings
handlers = ["console"]
if logs_exporter_envar := os.environ.get("OTEL_LOGS_EXPORTER"):
    handlers += ["otel"]


class OTELLoggingHandler(LoggingHandler):
    """Custom log handler that better handles the ProxyLogger

    If we haven't yet defined the logger provider (especially during forking processes like dramatiq)
    don't sweat about it and don't emit the log until it is configured.

    If we
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._disabled = os.environ.get("OTEL_SDK_DISABLED") or not os.environ.get(
            "OTEL_LOGS_EXPORTER"
        )
        self._configured = not isinstance(self._logger_provider, ProxyLoggerProvider)

    def emit(self, record: logging.LogRecord) -> None:
        if self._disabled:
            return

        if not self._configured:
            logger_provider = get_logger_provider()
            if logger_provider != self._logger_provider:
                self._logger_provider = logger_provider
                self._logger = get_logger(
                    __name__, logger_provider=self._logger_provider
                )
                self._configured = True

        # Do not emit logs if the logger provider is a proxy
        if isinstance(self._logger_provider, ProxyLoggerProvider):
            return None

        return super().emit(record)


class ExcludeAccessLogsFilter(logging.Filter):
    """Excludes access logs for things we don't care about"""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.args[2].removesuffix("/") not in (  # type: ignore
            "/",
            "/healthz",
            "/livez",
            "/readyz",
            "/pingz",
            "",
            "/favicon.ico",
        )  # type: ignore


DEFAULT_LOGGING_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s|%(levelname)-5s|%(name)-20s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "otel": {
            "class": "uptick_observability.logging.OTELLoggingHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": handlers,
        "level": "INFO",
        "formatter": "simple",
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": handlers,
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": handlers,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": handlers,
            "level": "INFO",
            "propagate": False,
            "filters": [ExcludeAccessLogsFilter()],
        },
    },
}
