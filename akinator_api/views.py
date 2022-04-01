from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from akinator_api import models
from akinator_api.serializers import CharacterSerializer


class CharacterView(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = models.Character.objects.all().order_by("-id")
