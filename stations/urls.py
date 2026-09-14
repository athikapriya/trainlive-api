from django.urls import path

from .views import *


urlpatterns = [
    path("", StationListAPIView.as_view(), name="station_list"),
]
