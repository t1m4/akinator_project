# Create your views here.
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from akinator_api import models, serializers


class IndexView(APIView):
    def get(self, request):
        return render(request, 'akinator_api/index.html')

class CharacterView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CharacterSerializer
    queryset = models.Character.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action in ["add_answers", "delete_answers"]:
            return serializers.CharacterAnswersSerializer
        return super().get_serializer_class()

    @action(
        detail=True, methods=["post", "get"], url_name="akinator-character-add_answers"
    )
    def add_answers(self, request, pk=None, *args, **kwargs):
        parent_object = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"parent_object": parent_object}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data)

    @action(
        detail=True,
        methods=["post", "get"],
        url_name="akinator-character-delete_answers",
    )
    def delete_answers(self, request, pk=None, *args, **kwargs):
        parent_object = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"parent_object": parent_object}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.delete(serializer.validated_data)
        return Response(response_data)


class QuestionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all().order_by("-id")


class UserGameViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.UserGameSerializer
    queryset = models.UserGame.objects.all().order_by("-id")

    @action(
        detail=True,
        methods=["post", "get"],
        url_name="akinator-character-game_add_answers",
    )
    def add_answers(self, request, pk=None, *args, **kwargs):
        parent_object = self.get_object()
        serializer = serializers.UserGameAnswerSerializer(
            data=request.data, context={"parent_object": parent_object}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data)
