from django.test import TestCase

from .models import Route


class RouteApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Route.objects.create(
            id="blue-line",
            name="Blue Line",
            origin="Central Station",
            destination="Tech Park",
            stops=["Central Station", "Market Square", "University", "Tech Park"],
            duration_min=22,
            frequency_min=12,
            service_label="Illustrative direct service",
        )
        Route.objects.create(
            id="green-line",
            name="Green Line",
            origin="Central Station",
            destination="University",
            stops=["Central Station", "Museum", "University"],
            duration_min=16,
            frequency_min=15,
            service_label="Illustrative direct service",
        )

    def test_health_endpoint_identifies_this_project(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["project"], "Bus Route Information System")
        self.assertEqual(response.json()["services"], ["routes"])

    def test_routes_endpoint_returns_ordered_records_and_data_notice(self):
        response = self.client.get("/api/routes/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 2)
        self.assertEqual(payload["items"][0]["id"], "green-line")
        self.assertIn("fictional sample data", payload["disclaimer"])

    def test_origin_and_destination_filters_are_case_insensitive(self):
        response = self.client.get("/api/routes/?origin=central%20station&destination=TECH%20PARK")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()["items"]], ["blue-line"])

    def test_search_matches_route_name(self):
        response = self.client.get("/api/routes/?q=blue")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()["items"]], ["blue-line"])

    def test_search_matches_intermediate_stop(self):
        response = self.client.get("/api/routes/?q=Museum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in response.json()["items"]], ["green-line"])

    def test_unknown_search_returns_empty_collection(self):
        response = self.client.get("/api/routes/?q=not-a-place")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"], [])
        self.assertEqual(response.json()["count"], 0)

    def test_write_methods_are_not_allowed(self):
        response = self.client.post("/api/routes/", data={})
        self.assertEqual(response.status_code, 405)
