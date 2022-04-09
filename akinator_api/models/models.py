from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
from akinator_api.models.base import ModelWithCreateAndUpdateDates


class Character(ModelWithCreateAndUpdateDates):
    name = models.CharField(max_length=256)
    answers = JSONField()
    questions_ids = JSONField(blank=True, null=True, default=list)
    image_url = models.URLField(blank=True, null=True)


class Question(ModelWithCreateAndUpdateDates):
    name = models.CharField(max_length=256)


class UserGame(ModelWithCreateAndUpdateDates):
    answers = JSONField(blank=True, default=list)
    questions_ids = JSONField(blank=True, null=True, default=list)
    predicted_character = models.ForeignKey(
        "akinator_api.Character", on_delete=models.DO_NOTHING, blank=True, null=True
    )
    is_success_predicted = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    user_answer = models.CharField(max_length=256, blank=True, null=True)
    user_character_id = models.IntegerField(blank=True, null=True)

    # ProbabilityService
    probabilities = JSONField(null=True, blank=True, default=dict)
