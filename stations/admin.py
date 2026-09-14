from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Station


@admin.register(Station)
class StationAdmin(LeafletGeoAdmin):

    list_display = (
        "id",
        "station_name",
        "name_en",
        "coordinates",
    )

    list_display_links = (
        "id",
        "station_name",
    )

    search_fields = (
        "name",
        "name_en",
    )

    ordering = ("name",)

    list_per_page = 50

    fieldsets = (
        (
            "Station Information",
            {
                "fields": (
                    "name",
                    "name_en",
                ),
            },
        ),
        (
            "Geographic Location",
            {
                "fields": ("geom",),
            },
        ),
    )

    @admin.display(
        description="Station Name",
        ordering="name",
    )
    def station_name(self, obj):
        return (
            obj.name
            or obj.name_en
            or f"Station #{obj.pk}"
        )

    @admin.display(description="Coordinates")
    def coordinates(self, obj):
        if obj.geom:
            return f"{obj.geom.y:.6f}, {obj.geom.x:.6f}"

        return "No location"