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
        fields = ('id', 'name')


class CharacterAnswersSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=False)

    def create(self, validated_data, *args, **kwargs):
        new_answers = validated_data.get('answers')
        parent_object = self.context['parent_object']
        for new_answer in new_answers:
            if new_answer in parent_object.answers:
                continue
            services.get_object_or_error(models.Question, new_answer['id'])
            parent_object.answers.append(new_answer)
        parent_object.save(update_fields=['answers'])
        return parent_object.answers

    def delete(self, validated_data, *args, **kwargs):
        delete_answers = validated_data.get('answers')
        parent_object = self.context['parent_object']
        for delete_answer in delete_answers:
            delete_answer_index = services.get_element_index_by_value(parent_object.answers, delete_answer)
            services.get_object_or_error(models.Question, delete_answer['id'])
            del parent_object.answers[delete_answer_index]
        parent_object.save(update_fields=['answers'])
        return parent_object.answers
