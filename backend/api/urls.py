from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("routes/", views.routes, name="routes"),
    path("routes/locations/", views.route_locations, name="route-locations"),
    path("routes/<slug:route_id>/", views.route_detail, name="route-detail"),
]
