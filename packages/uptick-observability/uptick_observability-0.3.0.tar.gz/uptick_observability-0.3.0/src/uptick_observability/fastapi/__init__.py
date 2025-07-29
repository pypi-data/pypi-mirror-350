import logging
import logging.config
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

logger = logging.getLogger(__name__)


def manually_instrument_fastapi(instrument_tracing: bool = True) -> None:
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
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor)

    # _DjangoMiddleware._excluded_urls = ExcludeList(settings.PATHS_WITHOUT_INSTRUMENTATION)
    # excluded_urls=excluded_urls

    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        FastAPIInstrumentor().instrument()
    except ImportError:
        logger.info("FastAPIInstrumentor not installed. Skipping instrumentation")

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
