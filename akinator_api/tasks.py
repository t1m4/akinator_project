from celery.task import task

from akinator_api import models
from services import image_parser_service


@task(name="parse_image_url")
def parse_image_url(character_id: int):
    character = models.Character.objects.get(id=character_id)
    driver_service = image_parser_service.WebDriver()
    image_url = driver_service.find(character.name)
    if image_url:
        character.image_url = image_url
        character.save(update_fields=['image_url'])