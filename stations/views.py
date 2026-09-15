from rest_framework import generics, filters
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Station
from .serializers import StationSerializer
from .paginations import StationPagination
from .permissions import (
    IsAuthenticatedForReadAdminForWrite,
    IsAdminOnly,
)


# =========================================================
# StationListAPIView section
# =========================================================
@extend_schema(
    tags=["Stations"],
)
@extend_schema(
    methods=["GET"],
    summary="List railway stations",
    description=(
        "Retrieve a paginated list of railway stations. "
        "Stations can be searched by Bengali or English name."
    ),
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search stations by Bengali or English name.",
            required=False,
            type=str,
        ),
    ],
)
@extend_schema(
    methods=["POST"],
    summary="Create a railway station",
    description=(
        "Create a new railway station. "
        "This operation requires admin access."
    ),
)
class StationListAPIView(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    pagination_class = StationPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_en']

    permission_classes = [IsAuthenticatedForReadAdminForWrite]


# =========================================================
# StationDetailAPIView section
# =========================================================
@extend_schema(
    tags=["Stations"],
)
@extend_schema(
    methods=["GET"],
    summary="Retrieve a railway station",
    description=(
        "Retrieve detailed information about a specific railway station. "
        "Authentication is required."
    ),
)
@extend_schema(
    methods=["PUT"],
    summary="Update a railway station",
    description=(
        "Completely update a railway station. "
        "This operation requires admin access."
    ),
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a railway station",
    description=(
        "Update one or more fields of a railway station without "
        "replacing the entire resource. This operation requires "
        "admin access."
    ),
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a railway station",
    description=(
        "Delete a railway station. "
        "This operation requires admin access."
    ),
)
class StationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    permission_classes = [IsAdminOnly]