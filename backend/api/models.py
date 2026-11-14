from django.db import models


class Route(models.Model):
    """A published route in the demonstration transit network."""

    id = models.SlugField(primary_key=True, max_length=80)
    name = models.CharField(max_length=120)
    origin = models.CharField(max_length=120, db_index=True)
    destination = models.CharField(max_length=120, db_index=True)
    stops = models.JSONField(default=list)
    duration_min = models.PositiveSmallIntegerField()
    frequency_min = models.PositiveSmallIntegerField()
    service_label = models.CharField(max_length=80, default="Sample service")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("duration_min", "name")

    def __str__(self):
        return f"{self.name}: {self.origin} → {self.destination}"
