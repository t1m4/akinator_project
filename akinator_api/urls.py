from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()

router.register("questions", views.QuestionView, basename="akinator-question")
character_router = router.register("character", views.CharacterView, basename="akinator-character")
urlpatterns = router.urls
