from django.core.management.base import BaseCommand

from api.models import Route


ROUTES = [
    {
        "id": "blue-line",
        "name": "Blue Line",
        "origin": "Central Station",
        "destination": "Tech Park",
        "stops": ["Central Station", "Market Square", "University", "Tech Park"],
        "duration_min": 22,
        "frequency_min": 12,
        "service_label": "Illustrative direct service",
    },
    {
        "id": "green-line",
        "name": "Green Line",
        "origin": "Central Station",
        "destination": "University",
        "stops": ["Central Station", "Museum", "University"],
        "duration_min": 16,
        "frequency_min": 15,
        "service_label": "Illustrative direct service",
    },
    {
        "id": "orange-line",
        "name": "Orange Line",
        "origin": "Riverside",
        "destination": "Tech Park",
        "stops": ["Riverside", "Market Square", "University", "Tech Park"],
        "duration_min": 25,
        "frequency_min": 18,
        "service_label": "Illustrative direct service",
    },
]


class Command(BaseCommand):
    help = "Load only the fictional route catalogue for the Wayfinder demo."

    def handle(self, *args, **options):
        for item in ROUTES:
            Route.objects.update_or_create(id=item["id"], defaults=item)
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(ROUTES)} fictional sample routes.")
        )
