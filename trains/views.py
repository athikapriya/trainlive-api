from rest_framework import generics, filters
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Train, TrainStation
from .serializers import TrainSerializers
from .paginations import TrainPagination
from .permissions import (
    IsAuthenticatedForReadAdminForWrite,
    IsAdminOnly,
)


# =========================================================
# TrainListAPIView section
# =========================================================
@extend_schema(
    tags=["Trains"],
)
@extend_schema(
    methods=["GET"],
    summary="List trains",
    description=(
        "Retrieve a paginated list of trains with their routes, "
        "stations, and scheduled arrival and departure times.\n\n"
        "Use the search parameter to search by train number, "
        "train name, or Bengali train name.\n\n"
        "Authentication is required."
    ),
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search trains by number, name, or Bengali name.",
            required=False,
            type=str,
        ),
    ],
)
@extend_schema(
    methods=["POST"],
    summary="Create a train",
    description=(
        "Create a new train. "
        "This operation requires admin access."
    ),
)
class TrainListAPIView(generics.ListCreateAPIView):
    queryset = Train.objects.prefetch_related(Prefetch("stops", queryset=TrainStation.objects.select_related("station")))
    serializer_class = TrainSerializers
    pagination_class = TrainPagination
    
    permission_classes = [IsAuthenticatedForReadAdminForWrite]

    filter_backends = [filters.SearchFilter]
    search_fields = ["number", 'name', 'name_bn']



# =========================================================
# TrainDetailAPiView section
# =========================================================
@extend_schema(
    tags=["Trains"],
)
@extend_schema(
    methods=["GET"],
    summary="Retrieve a train",
    description=(
        "Retrieve detailed information about a specific train, "
        "including its route, stations, and scheduled times. "
        "This operation requires admin access."
    ),
)
@extend_schema(
    methods=["PUT"],
    summary="Update a train",
    description=(
        "Completely update a train. "
        "This operation requires admin access."
    ),
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a train",
    description=(
        "Partially update a train without replacing the entire resource. "
        "This operation requires admin access."
    ),
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a train",
    description=(
        "Delete a train. "
        "This operation requires admin access."
    ),
)
class TrainDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Train.objects.prefetch_related(Prefetch("stops", queryset=TrainStation.objects.select_related("station")))
    serializer_class = TrainSerializers

    permission_classes = [IsAdminOnly]

    lookup_field = 'number'