from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class InfoModel(models.Model):
    all_prediction_count = models.IntegerField()
    count_of_characters = models.IntegerField()