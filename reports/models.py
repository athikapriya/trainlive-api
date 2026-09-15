from django.db import models
from django.conf import settings

from stations.models import Station
from trains.models import Train


# =========================================================
# Report Model section
# =========================================================
class Report(models.Model):
    class EventType(models.TextChoices):
        ARRIVED = "ARRIVED", "Arrived at station"
        DEPARTED = "DEPARTED", "Departed from station"
        PASSED = "PASSED", "Passed through"
        ISSUE = "ISSUE", "Issue"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="reports")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="reports", blank=True, null=True)

    event_time = models.DateTimeField()
    event_type = models.CharField(max_length=10, choices=EventType.choices)

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-event_time"]

        indexes = [
            models.Index(
                fields=["train", "-event_time"],
                name="report_train_time_idx",
            ),
            models.Index(
                fields=["station", "-event_time"],
                name="report_station_time_idx",
            ),
            models.Index(
                fields=["-event_time"],
                name="report_event_time_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.train} - "
            f"{self.get_event_type_display()} - "
            f"{self.event_time}"
        )



# =========================================================
# Report Vote section
# =========================================================
class ReportVote(models.Model):
    class Vote(models.TextChoices):
        RIGHT = "RIGHT", "Right"
        WRONG = "WRONG", "Wrong"

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_votes')

    vote = models.CharField(max_length=5, choices=Vote.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["report", "user"],
                name="unique_user_report_vote",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.vote} - "
            f"Report #{self.report_id}"
        )