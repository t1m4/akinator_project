import dataclasses
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


def main():
    creator = Creator()

    characters = [
        {"name": "Homer Simpson", "answers": {1: 1, 2: 1, 3: 1, 4: 0}},
        {"name": "SpongeBob SquarePants", "answers": {1: 1, 2: 1, 3: 1, 4: 0.75}},
        {"name": "Sandy Cheeks", "answers": {1: 0, 2: 0, 3: 0}},
    ]

    character_data = {
        "name": "Homer Simpson",
        "answers": [
            {
                "id": 1,
                "answer": 1,
            },
            {
                "id": 2,
                "answer": 1,
            },
            {
                "id": 3,
                "answer": 1,
            },
            {
                "id": 4,
                "answer": 0,
            },
        ],
    }
    character_data = {
        "name": "SpongeBob SquarePants",
        "answers": [
            {
                "id": 1,
                "answer": 1,
            },
            {
                "id": 2,
                "answer": 1,
            },
            {
                "id": 3,
                "answer": 1,
            },
            {
                "id": 4,
                "answer": 0.75,
            },
        ],
    }
    character_data = {
        "name": "Sandy Cheeks",
        "answers": [
            {
                "id": 1,
                "answer": 0,
            },
            {
                "id": 2,
                "answer": 0,
            },
            {
                "id": 3,
                "answer": 0,
            },
        ],
    }

    game_data = {
        "answers": [],
        "is_success_predicted": False,
        "is_finished": False,
        "user_answer": "",
        "user_character_id": None,
        "predicted_character": None,
    }

    answers_data = {
        "answers": [
            {
                "id": 2,
                "answer": 1,
            },
            # {
            #     'id': 2,
            #     'answer': 0.5,
            # }
        ]
    }
    character_id = "1"
    game_id = "4"
    response = creator.create_object(creator.create_character_url, character_data)
    # response = creator.create_object(creator.create_game_url, game_data)
    # response = creator.create_object(creator.add_character_answers_url.replace("<character_id>", character_id), answers_data)
    # response = creator.create_object(creator.delete_character_answers_url.replace("<character_id>", character_id), answers_data)
    # response = creator.create_object(
    #     creator.add_game_answers_url.replace("<game_id>", game_id), answers_data
    # )
    from services.probability_service import ProbabilityService

    # Procalculate_probabilities([], [])


if __name__ == "__main__":
    import os
    import sys

    sys.path.append("/home/ruslan/PycharmProjects/akinator_project")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akinator_platform.settings")
    import django

    django.setup()
    main()
