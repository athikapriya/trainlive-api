from django.db import models

from stations.models import Station


# ==============================================
# Train Model section
# ==============================================
class Train(models.Model):
    class Direction(models.TextChoices):
        UP = "UP", "Up"
        DOWN = "DOWN", 'Down'

    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    name_bn = models.CharField(max_length=100, blank=True)

    direction = models.CharField(max_length=4, choices=Direction.choices)
    off_day = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'{self.number} - {self.name}'



# ==============================================
# TrainStation Model section
# ==============================================
class TrainStation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="stops")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="train_stops")

    stop_order = models.PositiveIntegerField()

    scheduled_arrival = models.TimeField(null=True, blank=True)
    scheduled_departure = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["train", "stop_order"]

        constraints = [
            models.UniqueConstraint(
                fields = ["train", 'station'],
                name = "unique_train_station",
            ),
            models.UniqueConstraint(
                fields = ["train", "stop_order"],
                name = "unique_train_stop_order",
            ),
        ]

        indexes = [
            models.Index(
                fields=["train", "stop_order"],
                name="train_stop_order_idx",
            ),
            models.Index(
                fields=["station"],
                name="station_idx",
            ),
        ]

    def __str__(self):
        return f"{self.train} - {self.station}"