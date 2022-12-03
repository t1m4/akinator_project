import random

from ipware import get_client_ip
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
        if not validated_data.get("questions_ids"):
            answers = validated_data.get("answers")
            instance.questions_ids = [answer["id"] for answer in answers]
            instance.save(update_fields=["questions_ids"])

        if not validated_data.get("image_url"):
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
        read_only_fields = ("predicted_character", "probabilities")
        exclude = ("questions_ids", "ip_address")
        # exclude = ('probabilities', 'questions_ids')

    def create(self, validated_data):
        instance = super().create(validated_data)
        update_fields = []
        client_address, _ = get_client_ip(self.context['request'])
        if client_address:
            instance.ip_address = client_address
            update_fields.append('ip_address')
        if not validated_data.get("questions_ids"):
            answers = validated_data.get("answers")
            instance.questions_ids = [answer["id"] for answer in answers]
            update_fields.append("questions_ids")
        instance.save(update_fields=update_fields)
        return instance

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if not validated_data.get("questions_ids"):
            answers = validated_data.get("answers")
            instance.questions_ids = [answer["id"] for answer in answers]
            instance.save(update_fields=["questions_ids"])
        return instance


class UserGameAnswerSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True, required=True)

    def create(self, validated_data, *args, **kwargs):
        new_answers = validated_data.get("answers")
        game_object = self.context["parent_object"]
        answers = services.add_new_answers_to_object(new_answers, game_object)

        service_object = probability_service.ProbabilityService(game_object)
        probabilities = service_object.calculate_probabilities()

        answers_questions_ids = [answer["id"] for answer in answers]
        questions_left = models.Question.objects.exclude(
            id__in=answers_questions_ids
        ).values("id", "name")
        print("probabilities", probabilities)

        length_of_answers = len(game_object.answers)
        result = sorted(probabilities, key=lambda p: p["probability"], reverse=True)[0]
        if (
                len(questions_left) == 0
                or length_of_answers > 2
                and result["probability"] > 0.9
                or length_of_answers > 5
                and result["probability"] > 0.8
                or length_of_answers == 20
        ):
            return self.finish_game(game_object, result)
        else:
            next_question = service_object.find_next_question(probabilities, questions_left, answers_questions_ids)
            # next_question = None
            # if length_of_answers > 1:
            #     next_question_id = self._find_the_most_probable_question(
            #         probabilities, answers_questions_ids
            #     )
            #     if next_question_id == 'is_finished':
            #         return self.finish_game(game_object, result)
            #     if next_question_id:
            #         next_question = (
            #             questions_left.filter(id=next_question_id)
            #                 .values("id", "name")
            #                 .first()
            #         )
            if not next_question:
                next_question = random.choice(questions_left)
                # next_question = (
                #     questions_left.order_by("id").values("id", "name").first()
                # )
            return next_question

    @staticmethod
    def _find_the_most_probable_question(probabilities, answers_questions_ids):
        """
        TODO May me it's not a good idea to to so. But it's useful after many question. For examples, after 10 questions.
            We take most probable character, and ask his questions.
        """
        # character_id_with_most_probability = sorted(
        #     probabilities, key=lambda p: p["probability"], reverse=True
        # )[0]["id"]
        # character_with_most_probability = models.Character.objects.get(
        #     id=character_id_with_most_probability
        # )
        # for answer in character_with_most_probability.answers:
        #     character_question_id = answer['id']
        #     answer_value = answer['answer']
        #     print(answer)
        #     if character_question_id not in answers_questions_ids and answer_value > 0.75:
        #         print("return character question_", character_with_most_probability, character_question_id, "\n")
        #         return character_question_id

        characters_with_most_probability = sorted(
            probabilities, key=lambda p: p["probability"], reverse=True
        )
        next_character_probabilities = characters_with_most_probability[1]['probability']
        for index, character_probability in enumerate(characters_with_most_probability):
            if character_probability['probability'] > 100 * next_character_probabilities:
                return 'is_finished'
            character = models.Character.objects.get(
                id=character_probability['id']
            )
            for answer in character.answers:
                character_question_id = answer['id']
                answer_value = answer['answer']
                # print(next_character_probabilities, character_probability['probability'], answer)
                if character_question_id not in answers_questions_ids and answer_value > 0.75:
                    # print("return character question_", character, character_question_id, "\n")
                    return character_question_id
            next_character_probabilities = character_probability['probability']

    @staticmethod
    def finish_game(game_object, result):
        game_object.predicted_character = models.Character.objects.get(id=result["id"])
        game_object.save(update_fields=["predicted_character"])
        result["is_finished"] = True
        return result
