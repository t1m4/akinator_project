import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akinator_platform.settings")
app = Celery("akinator_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
