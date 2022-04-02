import dataclasses
import random
from abc import ABC

import requests


class Creator(ABC):
    host = "http://127.0.0.1:8000/"
    create_character_url = host + "api/character/"
    add_character_answers_url = host + "api/character/<character_id>/add_answers/"
    delete_character_answers_url = host + "api/character/<character_id>/delete_answers/"
    add_game_answers_url = host + "api/games/<game_id>/add_answers/"
    create_game_url = host + "api/games/"

    def create_object(self, url, data):
        if dataclasses.is_dataclass(data):
            data = data.get_json()
        response = requests.post(url, json=data)
        print(response.json())
        return response.json()

    def update_object(self, url, data):
        response = requests.put(url, json=data)
        print(response.json())
        return response


def index(question, answer):
    from akinator_api import models
    from akinator_api import services
    from services import probability_service

    # Save game answers
    user_game = models.UserGame.objects.get(id=5)
    services.add_new_answers_to_object([{"id": question, "answer": answer}], user_game)

    service_object = probability_service.ProbabilityService(user_game.answers)
    probabilities = service_object.calculate_probabilities()

    answers_questions_ids = [answer["id"] for answer in user_game.answers]
    questions_left = models.Question.objects.exclude(id__in=answers_questions_ids)
    if len(questions_left) == 0:
        result = sorted(probabilities, key=lambda p: p["probability"], reverse=True)[0]
        print(f"You got winner. This is your guess {result}")
        return models.Question(id=None)
    else:
        print(f"Left questions {questions_left}")
        # next_question = random.choice(questions_left)
        next_question = questions_left.order_by("id").first()
        return next_question


def main():
    from akinator_api import models

    user_game = models.UserGame.objects.get(id=5)
    user_game.answers = []
    user_game.save()

    questions = models.Question.objects.all().order_by("id")
    # next_question = random.choice(questions)
    next_question = questions.first()
    answer = input(next_question.name)
    while next_question.id:
        next_question = index(next_question.id, int(answer))
        if not next_question.id:
            break
        answer = input(
            f"Question number {next_question.id} and question: {next_question.name}"
        )


if __name__ == "__main__":
    import os
    import sys

    sys.path.append("/home/ruslan/PycharmProjects/akinator_project")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akinator_platform.settings")
    import django

    django.setup()
    main()
