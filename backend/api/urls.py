from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("routes/", views.routes, name="routes"),
    path("exercises/", views.exercises, name="exercises"),
    path("measurements/", views.measurements, name="measurements"),
]
