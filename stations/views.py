from rest_framework import generics, filters

from .models import Station
from .serializers import StationSerializer
from .paginations import StationPagination
from .permissions import IsAdminOrReadOnly


# =========================================================
# StationListAPIView section
# =========================================================
class StationListAPIView(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    pagination_class = StationPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_en']

    permission_classes = [IsAdminOrReadOnly]