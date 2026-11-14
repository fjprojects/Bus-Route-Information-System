from django.test import TestCase
from django.urls import reverse
from api.models import Route


class RouteApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Route.objects.create(
            id="blue-line",
            name="Blue Line",
            origin="Central Station",
            destination="Tech Park",
            stops=["Central Station", "University", "Tech Park"],
            duration_min=22,
            frequency_min=12,
        )
        Route.objects.create(
            id="green-line",
            name="Green Line",
            origin="Central Station",
            destination="University",
            stops=["Central Station", "Museum", "University"],
            duration_min=16,
            frequency_min=15,
        )

    def test_health_endpoint(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["framework"], "Django")

    def test_routes_endpoint_returns_records(self):
        response = self.client.get("/api/routes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(response.json()["items"][0]["id"], "green-line")

    def test_origin_and_destination_filters(self):
        response = self.client.get("/api/routes/?origin=Central%20Station&destination=Tech%20Park")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()["items"]], ["blue-line"])

    def test_search_filter(self):
        response = self.client.get("/api/routes/?q=Museum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()["items"]], ["green-line"])
