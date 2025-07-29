# Uptick-Observability
This repository contains our observability/instrumentation libraries for both django and fastapi projects.


# Instrumentation instructions
## Instrumenting Django
Django is instrumented primarily via opentelemetry logs/traces. Metrics are not yet supported.

1. Manually instrument `settings.py`

```python
MIDDLEWARE = [
    # ...
    "uptick_observability.django.middleware.AccessLoggingMiddleware",
    "uptick_observability.django.middleware.UptickSqlCounterDjangoMiddleware",
]

from uptick_observability.django import manually_instrument_django  # noqa
from uptick_observability.logging import manually_instrument_logging  # noqa

manually_instrument_django()
# By default it will inject the logging django config
manually_instrument_logging()
```

## Instrumenting Django/Dramatiq
1. Manually instrument in settings.py

```python

from uptick_observability.dramatiq import manually_instrument_dramatiq # noqa

manually_instrument_dramatiq()

```

## Instrumenting Django/Celery

1. Manually instrument in `settings.py`

```python

from uptick_observability.celery import manually_instrument_celery # noqa

manually_instrument_celery()
```

## Instrumenting FastAPI


```main.py
from uptick_observability.fastapi import manually_instrument_fastapi
from uptick_observability.logging import (
    DEFAULT_LOGGING_CONFIG_DICT,
    manually_instrument_logging,
)

logging.config.dictConfig(DEFAULT_LOGGING_CONFIG_DICT)
manually_instrument_logging()
manually_instrument_fastapi()

# before app is initiated
app = fastapi.FastAPI()
```


## Kubernetes setup / values
Environment variables required:

```
OTEL_PYTHON_LOG_CORRELATION = "true"
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED = "true"
OTEL_METRICS_EXPORTER = "none"
OTEL_EXPORTER_OTLP_TIMEOUT=1
OTEL_EXPORTER_OTLP_ENDPOINT = "https://quickwit-otel.onuptick.com/"
OTEL_LOGS_EXPORTER="otlp"
OTEL_TRACES_EXPORTER="otlp"

# Most important one to set. Use a separate name per component; eg: workforce-fg, workforge-bg
# We typically filter all dashboards on a service-name AND THEN DRILL DOWN either on a
# span attribute or a resource name
OTEL_SERVICE_NAME="workforce-fg"
OTEL_RESOURCE_ATTRIBUTES="release=arafire,environment=production"

# or
OTEL_SERVICE_NAME="logbooks-fg"
OTEL_RESOURCE_ATTRIBUTES="release=logbooks,environment=production"
```


# Contribution

## How do I
- How do I run test django server locally
`mise run django_otel` and `mise run dramatiq_otel` and `mise run celery_otel`


- How do I view the otel logs
[Grafana](https://grafana.onuptick.com/explore?schemaVersion=1&panes=%7B%22rz4%22%3A%7B%22datasource%22%3A%22a690c9f2-b753-4b27-a29a-335ce9d23742%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22datasource%22%3A%7B%22type%22%3A%22quickwit-quickwit-datasource%22%2C%22uid%22%3A%22a690c9f2-b753-4b27-a29a-335ce9d23742%22%7D%2C%22query%22%3A%22service_name%3A%5C%22otel-test%5C%22+%22%2C%22alias%22%3A%22%22%2C%22metrics%22%3A%5B%7B%22type%22%3A%22logs%22%2C%22id%22%3A%223%22%2C%22settings%22%3A%7B%22limit%22%3A%22200%22%2C%22sortDirection%22%3A%22desc%22%7D%7D%5D%2C%22bucketAggs%22%3A%5B%7B%22type%22%3A%22date_histogram%22%2C%22id%22%3A%222%22%2C%22settings%22%3A%7B%22interval%22%3A%22auto%22%7D%2C%22field%22%3A%22%22%7D%5D%2C%22timeField%22%3A%22%22%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-5m%22%2C%22to%22%3A%22now%22%7D%7D%7D&orgId=1)

