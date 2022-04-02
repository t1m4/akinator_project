from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()

router.register("questions", views.QuestionViewSet, basename="akinator-question")
router.register("games", views.UserGameViewSet, basename="akinator-games")
character_router = router.register("character", views.CharacterView, basename="akinator-character")
urlpatterns = router.urls
