from rest_framework import generics, filters
from django.db.models import Prefetch

from .models import Train, TrainStation
from .serializers import TrainSerializers
from .paginations import TrainPagination
from .permissions import IsAdminOrReadOnly


# =========================================================
# TrainListAPIView section
# =========================================================
class TrainListAPIView(generics.ListCreateAPIView):
    queryset = Train.objects.prefetch_related(Prefetch("stops", queryset=TrainStation.objects.select_related("station")))
    serializer_class = TrainSerializers
    pagination_class = TrainPagination
    
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["number", 'name', 'name_bn']
