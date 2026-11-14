from django.db import models


class Route(models.Model):
    """A demonstration route in the Wayfinder sample network."""

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


class ExerciseReference(models.Model):
    """A non-prescriptive movement-library entry for the Reform demo."""

    id = models.SlugField(primary_key=True, max_length=80)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, db_index=True)
    description = models.TextField()
    professional_note = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """A fictional walking-measurement record for descriptive demo views."""

    date = models.CharField(max_length=80, unique=True)
    left_step_time = models.DecimalField(max_digits=7, decimal_places=3)
    right_step_time = models.DecimalField(max_digits=7, decimal_places=3)
    walking_speed = models.DecimalField(max_digits=7, decimal_places=3)
    balance_score = models.DecimalField(max_digits=7, decimal_places=2)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.date
