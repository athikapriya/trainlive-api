from django.urls import path

from .views import *


urlpatterns = [
    path("", StationListAPIView.as_view(), name="station_list"),
    path("<int:pk>/", StationDetailAPIView.as_view(), name="station-detail"),
]
