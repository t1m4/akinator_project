from rest_framework import serializers

from akinator_api import models, services, tasks
from akinator_api.constants import ANSWER_CHOICES
from services import probability_service, image_parser_service


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
        instance = super().create(validated_data)
        if not validated_data.get('image_url'):
            tasks.parse_image_url.delay(instance.id)
        return instance


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
        read_only_fields = ("predicted_character", "probabilities")
        # exclude = ('probabilities',)


class UserGameAnswerSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=True)

    def create(self, validated_data, *args, **kwargs):
        new_answers = validated_data.get("answers")
        game_object = self.context["parent_object"]
        answers = services.add_new_answers_to_object(new_answers, game_object)

        service_object = probability_service.ProbabilityService(game_object)
        probabilities = service_object.calculate_probabilities()
        print('probabilities', probabilities)

        # TODO here we return new answers for user
        answers_questions_ids = [answer["id"] for answer in answers]
        questions_left = models.Question.objects.exclude(id__in=answers_questions_ids).values('id')

        # TODO change to the level of probabilities or some Constant variable depending from probability
        if len(questions_left) == 0:
            # TODO save game data to check, that we already finish the game
            result = sorted(probabilities, key=lambda p: p["probability"], reverse=True)[0]
            game_object.predicted_character = models.Character.objects.get(id=result['id'])
            game_object.save(update_fields=['predicted_character'])
            print(f"You got winner. This is your guess {result}")
            result['is_finished'] = True
            return result
        else:
            # TODO choose next question using more efficient algorithm
            # next_question = random.choice(questions_left)
            next_question = questions_left.order_by("id").values('id', 'name').first()
            print("left question", questions_left)
            return next_question
