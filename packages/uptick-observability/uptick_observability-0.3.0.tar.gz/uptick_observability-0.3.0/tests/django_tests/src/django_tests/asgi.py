"""
ASGI config for django_tests project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_tests.settings")

from uptick_observability.django import manually_instrument_django  # noqa
from uptick_observability.logging import manually_instrument_logging  # noqa
from opentelemetry.instrumentation.celery import CeleryInstrumentor

manually_instrument_django()
manually_instrument_logging()
CeleryInstrumentor().instrument()

application = get_asgi_application()
