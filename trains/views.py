from rest_framework import generics, filters

from .models import Train, TrainStation
from .serializers import TrainSerializers, TrainStationSerializers
from .paginations import TrainPagination
from .permissions import IsAdminOrReadOnly


# =========================================================
# TrainListAPIView section
# =========================================================
class TrainListAPIView(generics.ListCreateAPIView):
    queryset = Train.objects.all()
    serializer_class = TrainSerializers
    pagination_class = TrainPagination
    
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ["number", 'name', 'name_bn']
