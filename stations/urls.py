from django.urls import path

from .views import *


urlpatterns = [
    path("stations/", StationListAPIView.as_view(), name="station_list"),
]
