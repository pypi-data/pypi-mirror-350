"""Contains custom django settings configured from django settings"""

from django.conf import settings

# Controls the minimum duration of a span to be recorded
SQL_MINIMUM_SPAN_DURATION = getattr(
    settings, "UPTICK_OBSERVABILITY_SQL_MINIMUM_SPAN_DURATION", 100
)

REQUEST_DURATION_SLOW = getattr(
    settings, "UPTICK_OBSERVABILITY_REQUEST_DURATION_SLOW", 0.5
)
REQUEST_DURATION_VERY_SLOW = getattr(
    settings, "UPTICK_OBSERVABILITY_REQUEST_DURATION_VER_SLOW", 10
)

SQL_COUNT_SLOW = getattr(settings, "UPTICK_OBSERVABILITY_SQL_COUNT_SLOW", 25)
SQL_COUNT_VERY_SLOW = getattr(settings, "UPTICK_OBSERVABILITY_SQL_COUNT_VERY_SLOW", 100)

PATHS_WITHOUT_INSTRUMENTATION = getattr(
    settings,
    "UPTICK_OBSERVABILITY_PATHS_WITHOUT_INSTRUMENTATION",
    [
        "/healthcheck",
        "/healthcheck/",
        "/metrics",
        "/metrics/",
        "/health",
        "/healthz/",
        "/pingz",
        "/ping",
        "/readyz",
        "/readyz/",
        "/livez",
        "/livez/",
    ],
)
