import logging
import os

from celery import Celery

logger = logging.getLogger("test.celery")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_tests.settings")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# https://docs.celeryq.dev/projects/kombu/en/stable/reference/kombu.transport.redis.html#transport-options
app.conf.broker_transport_options["global_keyprefix"] = "CELERY"

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task(bind=True, ignore_result=True)
def hello_celery(self):
    logger.info("Hello from Celery")
