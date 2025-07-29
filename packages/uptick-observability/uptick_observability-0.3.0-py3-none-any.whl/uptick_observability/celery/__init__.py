from celery.signals import (
    setup_logging,  # noqa
)


@setup_logging.connect
def configure_logging(*args, **kwargs):
    """Configure logging for Celery for otel."""
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


def manually_instrument_celery():
    from opentelemetry.instrumentation.celery import CeleryInstrumentor

    CeleryInstrumentor().instrument()
