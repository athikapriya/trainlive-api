from django.contrib import admin

from .models import Train, TrainStation


# =========================================================
# TrainStation Inline
# =========================================================
class TrainStationInline(admin.TabularInline):
    model = TrainStation

    extra = 1

    ordering = ("stop_order",)

    fields = (
        "stop_order",
        "station",
        "scheduled_arrival",
        "scheduled_departure",
    )

    autocomplete_fields = ("station",)


# =========================================================
# Train Admin
# =========================================================
@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):

    list_display = (
        "number",
        "name",
        "name_bn",
        "direction",
        "off_day",
        "is_active",
        "stop_count",
    )

    list_filter = (
        "direction",
        "is_active",
        "off_day",
    )

    search_fields = (
        "number",
        "name",
        "name_bn",
    )

    ordering = (
        "number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Train Information",
            {
                "fields": (
                    "number",
                    "name",
                    "name_bn",
                    "direction",
                    "off_day",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [
        TrainStationInline,
    ]

    def stop_count(self, obj):
        return obj.stops.count()

    stop_count.short_description = "Stops"


# =========================================================
# TrainStation Admin
# =========================================================
@admin.register(TrainStation)
class TrainStationAdmin(admin.ModelAdmin):

    list_display = (
        "train",
        "stop_order",
        "station",
        "scheduled_arrival",
        "scheduled_departure",
    )

    list_filter = (
        "train",
        "station",
    )

    search_fields = (
        "train__number",
        "train__name",
        "train__name_bn",
        "station__name",
        "station__name_en",
    )

    ordering = (
        "train",
        "stop_order",
    )

    autocomplete_fields = (
        "train",
        "station",
    )