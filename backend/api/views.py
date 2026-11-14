from django import get_version
from django.db import DatabaseError, connection
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Route
from .pagination import error_response, paginate_items, text_parameter

PROJECT = "Bus Route Information System"
DISCLAIMER = (
    "Route names, stops, frequencies and journey times are fictional sample data. "
    "This API is not connected to a transport operator, official timetable, GPS, GTFS feed "
    "or live vehicle service. Do not use these values to plan a real journey."
)


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({
            "status": "degraded",
            "project": PROJECT,
            "database": "unavailable",
        }, status=503)

    return JsonResponse({
        "status": "ok",
        "project": PROJECT,
        "framework": "Django",
        "django_version": get_version(),
        "database": "connected",
        "services": ["routes"],
    })


@require_GET
def routes(request):
    origin, error = text_parameter(request, "origin", max_length=120)
    if error:
        return error
    destination, error = text_parameter(request, "destination", max_length=120)
    if error:
        return error
    query, error = text_parameter(request, "q", max_length=100)
    if error:
        return error

    sort, error = text_parameter(request, "sort", max_length=20)
    if error:
        return error
    order, error = text_parameter(request, "order", max_length=10)
    if error:
        return error

    sort = sort or "duration"
    order = order or "asc"
    sort_fields = {
        "duration": "duration_min",
        "frequency": "frequency_min",
        "name": "name",
    }
    if sort not in sort_fields:
        return error_response(
            "Use one of: duration, frequency, name.", parameter="sort"
        )
    if order not in {"asc", "desc"}:
        return error_response("Use 'asc' or 'desc'.", parameter="order")

    queryset = Route.objects.all()
    if origin:
        queryset = queryset.filter(origin__iexact=origin)
    if destination:
        queryset = queryset.filter(destination__iexact=destination)
    if query:
        stop_ids = [
            route.pk
            for route in queryset.only("id", "stops")
            if any(query.casefold() in str(stop).casefold() for stop in (route.stops or []))
        ]
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(origin__icontains=query)
            | Q(destination__icontains=query)
            | Q(id__in=stop_ids)
        )

    sort_field = sort_fields[sort]
    prefix = "-" if order == "desc" else ""
    queryset = queryset.order_by(f"{prefix}{sort_field}", "name")
    records = [
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

    page_items, pagination, error = paginate_items(request, records)
    if error:
        return error

    return JsonResponse({
        "project": PROJECT,
        "count": len(records),
        "items": page_items,
        "pagination": pagination,
        "filters": {
            "origin": origin or None,
            "destination": destination or None,
            "q": query or None,
        },
        "sort": {"by": sort, "order": order},
        "source": "fictional demonstration network",
        "disclaimer": DISCLAIMER,
    })
