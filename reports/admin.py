from django.contrib import admin

from .models import Report, ReportVote



# ==============================================
# Report section
# ==============================================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "train",
        "station",
        "event_type",
        "event_time",
        "user",
        "created_at",
    )

    list_filter = (
        "event_type",
        "train",
        "station",
        "event_time",
    )

    search_fields = (
        "train__number",
        "train__name",
        "train__name_bn",
        "station__name",
        "station__name_en",
        "user__username",
        "note",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-event_time",
    )

    list_per_page = 25


# ==============================================
# ReportVote section
# ==============================================
@admin.register(ReportVote)
class ReportVoteAdmin(admin.ModelAdmin):
    list_display = (
        "report",
        "user",
        "vote",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "vote",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "report__train__number",
        "report__train__name",
        "report__station__name",
        "report__station__name_en",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25