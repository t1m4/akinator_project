from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
from akinator_api.models.base import ModelWithCreateAndUpdateDates


class Character(ModelWithCreateAndUpdateDates):
    name = models.CharField(max_length=256)
    answers = JSONField()
    image_url = models.URLField()


class Question(ModelWithCreateAndUpdateDates):
    name = models.CharField(max_length=256)
