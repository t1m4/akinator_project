import numpy as np

from akinator_api import models


class ProbabilityService(object):
    def __init__(self, user_game: models.UserGame):
        self.user_game = user_game
        # self.user_answers = user_answers
        self.characters_count = models.Character.objects.all().count()
        self.characters = models.Character.objects.all().values("id", "answers", "name")

    def calculate_probabilities(self):
        probabilities = []
        for character in self.characters:
            probabilities.append(
                {
                    "id": character["id"],
                    "probability": self.calculate_character_probability(character),
                }
            )

        return probabilities

    def calculate_character_probability(self, character: dict):
        # Prior
        init_character_probability = 1 / self.characters_count

        # Likelihood
        character_previous_probabilities = self.user_game.probabilities.get(str(character['id']), {})
        character_total_probability = character_previous_probabilities.get('character_total_probability', 1)
        exclude_character_total_probability = character_previous_probabilities.get('exclude_character_total_probability', 1)

        user_answer = self.user_game.answers[-1]
        answer = float(user_answer["answer"])
        character_total_probability *= max(1 - abs(answer - self.character_answer(character, user_answer)), 0.01)
        p_answer_not_character = np.mean(
            [
                1 - abs(answer - self.character_answer(not_character, user_answer))
                for not_character in self.characters
                if not_character["id"] != character["id"]
            ]
        )
        exclude_character_total_probability *= max(p_answer_not_character, np.float64(0.01))
        self.save_probabilities(character, character_total_probability, exclude_character_total_probability)


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

    def save_probabilities(self, character, character_total_probability, exclude_character_total_probability):
        self.user_game.probabilities[character['id']] = {
            'character_total_probability': character_total_probability,
            'exclude_character_total_probability': exclude_character_total_probability,
        }
        self.user_game.save(update_fields=['probabilities'])