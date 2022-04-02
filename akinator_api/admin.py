from django.contrib import admin

# Register your models here.
from akinator_api import models


class CharacterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image_url", "answers"]


admin.site.register(models.Character, CharacterAdmin)
admin.site.register(models.Question)
admin.site.register(models.UserGame)
