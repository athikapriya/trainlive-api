from django.contrib.gis.db import models


# =========================================================
# station Model section
# =========================================================
class Station(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)

    geom = models.PointField(srid=4326)

    class Meta:
        verbose_name = "Railway Station"
        verbose_name_plural = "Railway Stations"

        ordering = ["name"]

        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=["name_en"]),
        ]

    def __str__(self):
        if self.name and self.name_en:
            return f'{self.name} - {self.name_en}'
        return self.name or self.name_en or f"Station #{self.pk}"
