from random import choices

from rest_framework import serializers

from akinator_api import models
from akinator_api.constants import ANSWER_CHOICES


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=ANSWER_CHOICES)


class CharacterSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Character
        fields = ('id', 'name', 'answers')
        read_only = ('image_url')

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)