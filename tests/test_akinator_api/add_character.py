import dataclasses
from abc import ABC

import requests


class Creator(ABC):
    host = "http://127.0.0.1:8000/"
    create_character_url = host + "api/character"
    add_character_answers_url = host + "api/character/<character_id>/add_answers/"
    delete_character_answers_url = host + "api/character/<character_id>/delete_answers/"
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
    game_data = {
        "answers": [],
        "is_success_predicted": False,
        "is_finished": False,
        "user_answer": "",
        # "user_character_id": None,
        # "predicted_character": None
    }
    response = creator.create_object(creator.create_game_url, game_data)


if __name__ == "__main__":
    import os
    import sys

    sys.path.append('/home/ruslan/PycharmProjects/akinator_project')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "akinator_platform.settings")
    import django

    django.setup()
    main()
