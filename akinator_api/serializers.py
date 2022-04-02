from rest_framework import serializers

from akinator_api import models, services
from akinator_api.constants import ANSWER_CHOICES


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.ChoiceField(choices=ANSWER_CHOICES)


class CharacterSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, allow_empty=False)

    class Meta:
        model = models.Character
        fields = ("id", "name", "answers", "image_url")
        read_only_fields = ("image_url",)

    def create(self, validated_data):
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ("id", "name")


class CharacterAnswersSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=True)

    def create(self, validated_data, *args, **kwargs):
        new_answers = validated_data.get("answers")
        parent_object = self.context["parent_object"]
        answers = services.add_new_answers_to_object(new_answers, parent_object)
        return answers

    def delete(self, validated_data, *args, **kwargs):
        delete_answers = validated_data.get("answers")
        parent_object = self.context["parent_object"]
        answers = services.delete_answers_from_object(delete_answers, parent_object)
        return answers


class UserGameSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, allow_empty=True)

    class Meta:
        model = models.UserGame
        fields = "__all__"


class UserGameAnswerSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=True)

    def create(self, validated_data, *args, **kwargs):
        new_answers = validated_data.get("answers")
        parent_object = self.context["parent_object"]
        answers = services.add_new_answers_to_object(new_answers, parent_object)
        # TODO here we return new answers for user
        return answers
