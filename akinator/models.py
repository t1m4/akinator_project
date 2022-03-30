from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=256)
    answers = JSONField()
    image_url = models.URLField()


class Question(models.Model):
    name = models.CharField(max_length=256)


class InfoModel(models.Model):
    all_prediction_count = models.IntegerField()
    count_of_characters = models.IntegerField()