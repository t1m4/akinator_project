import math

import numpy as np

from akinator_api import models, constants


class ProbabilityService(object):
    def __init__(self, user_game: models.UserGame):
        self.user_game = user_game
        # self.user_answers = user_answers
        self.characters_count = models.Character.objects.all().count()
        self.characters = models.Character.objects.all().values("id", "answers", "name")
        self.is_save_probabilities = True

    def calculate_probabilities(self, custom_user_answer=None):
        probabilities = []
        for character in self.characters:
            probabilities.append(
                {
                    "id": character["id"],
                    "probability": self.calculate_character_probability(character, custom_user_answer),
                }
            )

        return probabilities

    def calculate_character_probability(self, character: dict, custom_user_answer=None):
        # Prior
        init_character_probability = 1 / self.characters_count

        # Likelihood
        character_previous_probabilities = self.user_game.probabilities.get(
            str(character["id"]), {}
        )
        character_total_probability = character_previous_probabilities.get(
            "character_total_probability", 1
        )
        exclude_character_total_probability = character_previous_probabilities.get(
            "exclude_character_total_probability", 1
        )

        if self.is_save_probabilities:
            user_answer = self.user_game.answers[-1]
        else:
            user_answer = custom_user_answer
        answer = float(user_answer["answer"])
        character_total_probability *= max(
            1 - abs(answer - self.character_answer(character, user_answer)), 0.01
        )
        p_answer_not_character = np.mean(
            [
                1 - abs(answer - self.character_answer(not_character, user_answer))
                for not_character in self.characters
                if not_character["id"] != character["id"]
            ]
        )
        exclude_character_total_probability *= max(
            p_answer_not_character, np.float64(0.01)
        )
        if self.is_save_probabilities:
            self.save_probabilities(
                character, character_total_probability, exclude_character_total_probability
            )

        # Evidence
        independent_probability = (
                character_total_probability * init_character_probability
                + (1 - init_character_probability) * exclude_character_total_probability
        )
        # Bayes Theorem
        inverse_probability = (
                                      character_total_probability * init_character_probability
                              ) / independent_probability
        return inverse_probability

    @staticmethod
    def character_answer(character: dict, question: dict):
        for answer in character["answers"]:
            if question["id"] == answer["id"]:
                return answer["answer"]
        return 0.5

    def save_probabilities(
            self,
            character,
            character_total_probability,
            exclude_character_total_probability,
    ):
        self.user_game.probabilities[character["id"]] = {
            "character_total_probability": character_total_probability,
            "exclude_character_total_probability": exclude_character_total_probability,
        }
        self.user_game.save(update_fields=["probabilities"])

    def _calculate_entropy(self, probabilities):
        result = 0
        for probability in probabilities:
            result += probability['probability'] * math.log(probability['probability'], 2)
        return result * -1

    def find_next_question(self, probabilities, questions_left, answers_questions_ids):
        current_entropy = self._calculate_entropy(probabilities)
        characters_with_most_probability = sorted(
            probabilities, key=lambda p: p["probability"], reverse=True
        )[0]['id']
        character_with_most_probability = models.Character.objects.get(id=characters_with_most_probability)
        self.is_save_probabilities = False

        best_entropy = current_entropy
        next_question = None
        for question in questions_left:
            for answer in constants.ANSWER_PROBABILITY_LIST:
                custon_user_answer = {
                    'id': question['id'],
                    'answer': answer,
                }
                new_probabilities = self.calculate_probabilities(custon_user_answer)
                new_entropy = self._calculate_entropy(new_probabilities)
                if new_entropy < best_entropy:
                    best_entropy = new_entropy
                    next_question = question
        print("new - {}, old = {}".format(best_entropy, current_entropy))
        if not next_question:
            for answer in character_with_most_probability.answers:
                character_question_id = answer['id']
                answer_value = answer['answer']
                if character_question_id not in answers_questions_ids and answer_value >= 0.75:
                    next_question = questions_left.filter(id=answer['id']).values("id", "name").first()

        return next_question