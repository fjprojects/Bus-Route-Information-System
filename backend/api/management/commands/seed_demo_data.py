from django.core.management.base import BaseCommand
from api.models import ExerciseReference, Measurement, Route


ROUTES = [
    {
        "id": "blue-line", "name": "Blue Line",
        "origin": "Central Station", "destination": "Tech Park",
        "stops": ["Central Station", "Market Square", "University", "Tech Park"],
        "duration_min": 22, "frequency_min": 12,
        "service_label": "Illustrative direct service",
    },
    {
        "id": "green-line", "name": "Green Line",
        "origin": "Central Station", "destination": "University",
        "stops": ["Central Station", "Museum", "University"],
        "duration_min": 16, "frequency_min": 15,
        "service_label": "Illustrative direct service",
    },
    {
        "id": "orange-line", "name": "Orange Line",
        "origin": "Riverside", "destination": "Tech Park",
        "stops": ["Riverside", "Market Square", "University", "Tech Park"],
        "duration_min": 25, "frequency_min": 18,
        "service_label": "Illustrative direct service",
    },
]

EXERCISES = [
    {
        "id": "shoulder-raise", "name": "Shoulder raise",
        "category": "Upper-body mobility",
        "description": "An illustrative upper-body movement reference for demonstrating a structured digital library.",
        "professional_note": "Only consider movements selected for you by a qualified healthcare professional. The application does not assess suitability.",
        "sort_order": 1,
    },
    {
        "id": "seated-knee-extension", "name": "Seated knee extension",
        "category": "Lower-body movement",
        "description": "An illustrative lower-body movement reference. This entry does not define repetitions, intensity or a personal programme.",
        "professional_note": "Use only as part of a plan supplied by a qualified healthcare professional.",
        "sort_order": 2,
    },
    {
        "id": "ankle-mobility", "name": "Ankle mobility",
        "category": "Gentle ankle movement",
        "description": "An example catalogue entry showing how movement information can be organised by category.",
        "professional_note": "A qualified healthcare professional should determine whether this movement is appropriate and provide any instructions.",
        "sort_order": 3,
    },
]

MEASUREMENTS = [
    ("Sample 01", "0.600", "0.620", "0.780", "76.00"),
    ("Sample 02", "0.590", "0.610", "0.830", "78.00"),
    ("Sample 03", "0.580", "0.600", "0.910", "80.00"),
    ("Sample 04", "0.610", "0.600", "0.880", "79.00"),
    ("Sample 05", "0.570", "0.590", "1.020", "83.00"),
    ("Sample 06", "0.560", "0.580", "1.080", "86.00"),
]


class Command(BaseCommand):
    help = "Load fictional sample data for the three portfolio demonstration APIs."

    def handle(self, *args, **options):
        for item in ROUTES:
            Route.objects.update_or_create(id=item["id"], defaults=item)
        for item in EXERCISES:
            ExerciseReference.objects.update_or_create(id=item["id"], defaults=item)
        for index, row in enumerate(MEASUREMENTS, start=1):
            Measurement.objects.update_or_create(
                date=row[0],
                defaults={
                    "left_step_time": row[1],
                    "right_step_time": row[2],
                    "walking_speed": row[3],
                    "balance_score": row[4],
                    "sort_order": index,
                },
            )
        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(ROUTES)} routes, {len(EXERCISES)} movement references and "
            f"{len(MEASUREMENTS)} fictional measurements."
        ))
