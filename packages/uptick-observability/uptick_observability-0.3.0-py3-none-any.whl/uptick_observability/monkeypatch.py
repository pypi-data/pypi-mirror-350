# Remove when: https://github.com/open-telemetry/opentelemetry-python/issues/3309
# This monkeypatch whill break when the issue is resolved so it should be obvious when to remove it.

# TLDR: OTEL exporter uses a backoff generator to retry sending data. It uses a SLEEP which is terrible
# and prevents the server from closing when the process is stopped. This monkeypatch was taken from the
# github issue. It keeps the retry but limits the number of retries to 2. This is a temporary fix until
# they fix the underlying sleep mechanic (this issue has been open for a while however...)
import logging
from typing import Any

import opentelemetry.exporter.otlp.proto.common._internal
import opentelemetry.exporter.otlp.proto.grpc.exporter
from opentelemetry.exporter.otlp.proto.common._internal import (
    _create_exp_backoff_generator,  # this is a copy
)


def _patched_otel_create_exp_backoff_generator(*args: Any, **kwargs: Any) -> Any:
    original_max_value = kwargs.get("max_value", 0)
    new_max_value = 2
    kwargs["max_value"] = new_max_value

    for backoff in _create_exp_backoff_generator(*args, **kwargs):
        yield backoff
        if backoff == new_max_value:
            if original_max_value:
                yield original_max_value  # the original function will stop if we return its max value
            break


opentelemetry.exporter.otlp.proto.common._internal._create_exp_backoff_generator = (
    opentelemetry.exporter.otlp.proto.grpc.exporter._create_exp_backoff_generator  # type: ignore
) = _patched_otel_create_exp_backoff_generator


# Monkey patch 2
# Exception while exporting logs: Invalid type {type(value)} of value {value} #3389
# This logger setting disables exporting the above warning messages because they are noiiiiisy
# https://github.com/open-telemetry/opentelemetry-python/issues/3389

logging.getLogger("opentelemetry.attributes").setLevel(logging.ERROR)
