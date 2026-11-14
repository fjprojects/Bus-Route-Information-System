from django import get_version
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Route

PROJECT = "Bus Route Information System"
DISCLAIMER = (
    "Route names, stops, frequencies and journey times are fictional sample data. "
    "This API is not connected to a transport operator, official timetable, GPS or live vehicle feed."
)


@require_GET
def health(request):
    return JsonResponse({
        "status": "ok",
        "project": PROJECT,
        "framework": "Django",
        "django_version": get_version(),
    })


@require_GET
def routes(request):
    queryset = Route.objects.all()
    origin = request.GET.get("origin", "").strip()
    destination = request.GET.get("destination", "").strip()
    query = request.GET.get("q", "").strip()

    if origin:
        queryset = queryset.filter(origin__iexact=origin)
    if destination:
        queryset = queryset.filter(destination__iexact=destination)
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(origin__icontains=query)
            | Q(destination__icontains=query)
        )

    items = [
        {
            "id": route.id,
            "name": route.name,
            "origin": route.origin,
            "destination": route.destination,
            "stops": route.stops,
            "duration_min": route.duration_min,
            "frequency_min": route.frequency_min,
            "service_label": route.service_label,
        }
        for route in queryset
    ]
    return JsonResponse({
        "project": PROJECT,
        "count": len(items),
        "items": items,
        "source": "fictional demonstration network",
        "disclaimer": DISCLAIMER,
    })
