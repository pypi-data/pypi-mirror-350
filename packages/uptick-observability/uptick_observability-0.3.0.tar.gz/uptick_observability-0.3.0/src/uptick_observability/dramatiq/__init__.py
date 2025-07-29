"""Instrumentation is handled by manually injecting the middlewares."""

from django.conf import settings  # type: ignore

middleware_name = "uptick_observability.dramatiq.middleware.OTELMiddleware"
("uptick_observability.dramatiq.middleware.MessageLoggingMiddleware",)


def manually_instrument_dramatiq():
    if middleware_name in settings.DRAMATIQ_BROKER.get("MIDDLEWARE", []):
        return

    settings.DRAMATIQ_BROKER["MIDDLEWARE"].insert(
        0, "uptick_observability.dramatiq.middleware.MessageLoggingMiddleware"
    )
    settings.DRAMATIQ_BROKER["MIDDLEWARE"].insert(
        0, "uptick_observability.dramatiq.middleware.UptickSqlCounterDramatiqMiddleware"
    )
    settings.DRAMATIQ_BROKER["MIDDLEWARE"].insert(
        0, "uptick_observability.dramatiq.middleware.OTELMiddleware"
    )
