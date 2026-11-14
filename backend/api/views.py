from django import get_version
from django.http import JsonResponse
from django.views.decorators.http import require_GET
PROJECT="Bus Route Information System"
DISCLAIMER="All route names, stops, frequencies and journey times are fictional sample data. This API is not connected to a transport operator, official timetable, GPS or live vehicle feed."
ITEMS=[
  {
    "id": "blue-line",
    "name": "Blue Line",
    "origin": "Central Station",
    "destination": "Tech Park",
    "stops": [
      "Central Station",
      "Market Square",
      "University",
      "Tech Park"
    ],
    "duration_min": 22,
    "frequency_min": 12
  },
  {
    "id": "green-line",
    "name": "Green Line",
    "origin": "Central Station",
    "destination": "University",
    "stops": [
      "Central Station",
      "Museum",
      "University"
    ],
    "duration_min": 16,
    "frequency_min": 15
  },
  {
    "id": "orange-line",
    "name": "Orange Line",
    "origin": "Riverside",
    "destination": "Tech Park",
    "stops": [
      "Riverside",
      "Market Square",
      "University",
      "Tech Park"
    ],
    "duration_min": 25,
    "frequency_min": 18
  }
]
@require_GET
def health(request):
    return JsonResponse({"status":"ok","project":PROJECT,"framework":"Django","django_version":get_version()})
@require_GET
def routes(request):
    return JsonResponse({"project":PROJECT,"items":ITEMS,"source":"fictional starter dataset","disclaimer":DISCLAIMER})
