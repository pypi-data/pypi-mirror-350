"""OpenTelemetry initialization module.

We do not use opentelemetry auto instrumentation because it is not compatible with pre-forking applications.

We need to specifically configure opentelemetry for our application after the process is forked (for dramatiq)
and after django has loaded for (daphne).
"""

# Patch Number 2
# Because we are using a multitenanting system, we want to add the workspace to the trace
# that would otherwise be missing.
import logging
import logging.config
import os
from typing import Any

from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import ReadableSpan, Span, TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

logger = logging.getLogger(__name__)


def get_view_name(request: Any) -> str:
    """The same logic that django_prometheus uses to get the view name."""
    view_name = "<unnamed view>"
    if hasattr(request, "resolver_match"):
        if request.resolver_match is not None:
            if request.resolver_match.view_name is not None:
                view_name = request.resolver_match.view_name
    return view_name


def custom_django_response_hook(span: Span, request: Any, response: Any) -> None:
    if user := getattr(request, "user", None):
        if user.id:
            span.set_attribute("user_id", user.id)

    if sql_count := getattr(response, "sql_count", None):
        span.set_attribute("sql_count", sql_count)

    if tenant := getattr(request, "tenant", None):
        span.set_attribute("workspace", tenant.name or "default")

    if view_name := get_view_name(request):
        span.set_attribute("view", view_name)

    # We track error count manually for easier quickwit aggregation
    if response.status_code >= 500:
        span.set_attribute("error_count", 1)

    # We track the uptick user email if they are logged in
    if session := getattr(request, "session", None):
        if user := getattr(request, "user", None):
            if email := getattr(user, "email", None):
                span.set_attribute("uptick.user.email", email)
        elif uptick_user_email := session.get("uptick_user_email"):
            span.set_attribute("uptick.user.email", uptick_user_email)


class UptickBatchSpanProcessor(BatchSpanProcessor):
    """Custom span processor that:
    1) filters out spans we don't care about
    2) and adds the workspace to all spans
    """

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        super().on_start(span, parent_context)

    def on_end(self, span: ReadableSpan) -> None:
        from . import settings

        # Ignore any home spans
        if span.instrumentation_scope:
            if span.attributes:
                # Ignore any spans that are for outbound analytics
                if http_url := span.attributes.get("http.url"):
                    excluded_sites = ["sentry.io", "launchdarkly.com", "mixpanel.com"]
                    if any(url in str(http_url) for url in excluded_sites):
                        return

            if (
                span.instrumentation_scope.name
                == "opentelemetry.instrumentation.psycopg2"
            ):
                # We don't want sql spans without a parent trace as it is too noisy
                if not span.parent:
                    return

                # We don't want sql spans that are too short of a duration
                if span.end_time and span.start_time:
                    duration_ms = (span.end_time - span.start_time) // 1_000_000
                    if duration_ms < settings.SQL_MINIMUM_SPAN_DURATION:
                        return

        super().on_end(span)


def manually_instrument_django(instrument_tracing: bool = True) -> None:
    """Manually configure opentelemetry

    Configuration is done via environment variables.

    The logger provider and trace provider are the standard default configuration
    that we would get from `opentelemetry-instrument`.

    # Documentation: https://opentelemetry-python-contrib.readthedocs.io/en/latest/_modules/opentelemetry/instrumentation/django.html
    """

    if os.environ.get("OTEL_SDK_DISABLED"):
        return

    if not isinstance(trace.get_tracer_provider(), trace.ProxyTracerProvider):
        return

    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)

    if traces_exporter_envar := os.environ.get("OTEL_TRACES_EXPORTER"):
        if instrument_tracing:
            otlp_exporter: SpanExporter = InMemorySpanExporter()
            if traces_exporter_envar == "otlp":
                otlp_exporter = OTLPSpanExporter()
            elif traces_exporter_envar == "console":
                otlp_exporter = ConsoleSpanExporter()
            span_processor = UptickBatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)

    from opentelemetry.instrumentation.django import (
        DjangoInstrumentor,
    )

    DjangoInstrumentor().instrument(
        response_hook=custom_django_response_hook,
        # comma separated list of urls to exclude from tracing
    )

    # _DjangoMiddleware._excluded_urls = ExcludeList(settings.PATHS_WITHOUT_INSTRUMENTATION)
    # excluded_urls=excluded_urls

    try:
        from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

        BotocoreInstrumentor().instrument()  # type: ignore[no-untyped-call]
    except ImportError:
        logger.info("BotocoreInstrumentor not installed. Skipping instrumentation")
    try:
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

        Psycopg2Instrumentor().instrument(skip_dep_check=True)
    except ImportError:
        logger.info("Psycopg2Instrumentor not installed. Skipping instrumentation")

    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        RequestsInstrumentor().instrument()
    except ImportError:
        logger.info("RequestsInstrumentor not installed. Skipping instrumentation")

    try:
        from opentelemetry.instrumentation.urllib import URLLibInstrumentor

        URLLibInstrumentor().instrument()
    except ImportError:
        logger.info("URLLibInstrumentor not installed. Skipping instrumentation")

    try:
        from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

        URLLib3Instrumentor().instrument()
    except ImportError:
        logger.info("URLLib3Instrumentor not installed. Skipping instrumentation")
