from django.urls import path

from .views import *


urlpatterns = [
    path("", TrainListAPIView.as_view(), name="train_list"),
]
