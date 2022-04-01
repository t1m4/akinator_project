from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView

from akinator.forms import QuestionForm


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        form = QuestionForm()
        return render(request, "akinator/index.html", context={"form": form})
