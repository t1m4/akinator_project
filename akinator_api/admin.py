from django.contrib import admin

# Register your models here.
from akinator_api import models


class CharacterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image_url", "answers"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class UserGameAdmin(admin.ModelAdmin):
    list_display = ["id", "answers", "predicted_character", "is_success_predicted", "is_finished", "user_answer", "user_character_id"]


admin.site.register(models.Character, CharacterAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.UserGame, UserGameAdmin)
