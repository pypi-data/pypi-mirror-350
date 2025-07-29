"""
URL configuration for django_tests project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import logging
import time

from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import path
from opentelemetry.trace import get_tracer

from django_tests.celery import hello_celery
from django_tests.core.tasks import hello_world_task

tracer = get_tracer(__name__)


def view(request):
    logging.info("hi testing logs")
    r = User.objects.all()
    list(r)
    with tracer.start_as_current_span("inner_span"):
        logging.info("more logs")
        time.sleep(0.2)
    logging.info("more logs")
    return HttpResponse("")


def readyz(request):
    return HttpResponse("")


def test_dramatiq(request):
    hello_world_task.send("william")
    return HttpResponse("")


def test_celery(request):
    hello_celery.delay()
    return HttpResponse("")


urlpatterns = [
    path("test_view", view),
    path("admin/", admin.site.urls),
    path("test_dramatiq/", test_dramatiq),
    path("test_celery/", test_celery),
    path("readyz/", readyz),
    path("readyz", readyz),
]
