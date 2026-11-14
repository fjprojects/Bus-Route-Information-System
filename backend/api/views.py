from django import get_version
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import ExerciseReference, Measurement, Route

DISCLAIMER_ROUTES = (
    "Route names, stops, frequencies and journey times are fictional sample data. "
    "This API is not connected to a transport operator, official timetable, GPS or live vehicle feed."
)
DISCLAIMER_EXERCISES = (
    "These are illustrative movement-library entries, not exercise prescriptions. "
    "The application does not analyse camera footage, assess recovery or diagnose conditions. "
    "Follow guidance from a qualified healthcare professional."
)
DISCLAIMER_MEASUREMENTS = (
    "These are fictional example measurements. This API is descriptive only: "
    "it does not calculate fall risk, make predictions, diagnose conditions or provide a medical assessment."
)


@require_GET
def health(request):
    return JsonResponse({
        "status": "ok",
        "project": "Portfolio demonstration API",
        "framework": "Django",
        "django_version": get_version(),
        "services": ["routes", "exercises", "measurements"],
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
        searchable_routes = queryset.filter(
            Q(name__icontains=query)
            | Q(origin__icontains=query)
            | Q(destination__icontains=query)
        )
        matched_ids = set(searchable_routes.values_list("id", flat=True))
        if len(query) >= 2:
            matched_ids.update(
                route.id for route in queryset
                if any(query.casefold() in stop.casefold() for stop in route.stops)
            )
        queryset = queryset.filter(id__in=matched_ids)

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
        "project": "Bus Route Information System",
        "count": len(items),
        "items": items,
        "source": "fictional demonstration network",
        "disclaimer": DISCLAIMER_ROUTES,
    })


@require_GET
def exercises(request):
    queryset = ExerciseReference.objects.all()
    category = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()
    if category and category.lower() != "all":
        queryset = queryset.filter(category__iexact=category)
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(category__icontains=query)
            | Q(description__icontains=query)
        )
    items = [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "description": item.description,
            "professional_note": item.professional_note,
        }
        for item in queryset
    ]
    return JsonResponse({
        "project": "AI Recovery Assistant",
        "count": len(items),
        "items": items,
        "source": "illustrative reference catalogue",
        "disclaimer": DISCLAIMER_EXERCISES,
    })


@require_GET
def measurements(request):
    items = [
        {
            "date": item.date,
            "left_step_time": float(item.left_step_time),
            "right_step_time": float(item.right_step_time),
            "walking_speed": float(item.walking_speed),
            "balance_score": float(item.balance_score),
        }
        for item in Measurement.objects.all()
    ]
    return JsonResponse({
        "project": "GaitGuardian",
        "count": len(items),
        "items": items,
        "source": "fictional demonstration dataset",
        "disclaimer": DISCLAIMER_MEASUREMENTS,
    })
