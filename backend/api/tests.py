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

    def test_health_endpoint_identifies_project_and_database(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["project"], "Bus Route Information System")
        self.assertEqual(response.json()["database"], "connected")
        self.assertIn("locations", response.json()["services"])

    def test_route_locations_expose_separate_selector_options(self):
        response = self.client.get("/api/routes/locations/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["origins"], ["Central Station"])
        self.assertEqual(payload["destinations"], ["Tech Park", "University"])
        self.assertIn("Museum", payload["stops"])
        self.assertEqual(payload["count"], len(payload["locations"]))

    def test_route_locations_are_unique_and_sorted(self):
        response = self.client.get("/api/routes/locations/")
        locations = response.json()["locations"]
        self.assertEqual(len(locations), len(set(locations)))
        self.assertEqual(locations, sorted(locations, key=str.casefold))

    def test_route_detail_returns_one_route(self):
        response = self.client.get("/api/routes/blue-line/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["item"]["id"], "blue-line")
        self.assertEqual(response.json()["item"]["stops"][1], "Market Square")

    def test_route_detail_returns_structured_404(self):
        response = self.client.get("/api/routes/missing-line/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"]["code"], "not_found")

    def test_routes_endpoint_returns_ordered_records_and_data_notice(self):
        response = self.client.get("/api/routes/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["count"], 2)
        self.assertEqual(payload["items"][0]["id"], "green-line")
        self.assertEqual(payload["pagination"]["total_items"], 2)
        self.assertIn("fictional sample data", payload["disclaimer"])

    def test_origin_and_destination_filters_are_case_insensitive(self):
        response = self.client.get(
            "/api/routes/?origin=central%20station&destination=TECH%20PARK"
        )
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
        self.assertEqual(response.json()["pagination"]["total_pages"], 0)

    def test_frequency_sort_and_descending_order(self):
        response = self.client.get("/api/routes/?sort=frequency&order=desc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["items"][0]["id"], "green-line")
        self.assertEqual(response.json()["sort"], {"by": "frequency", "order": "desc"})

    def test_pagination_preserves_total_count(self):
        response = self.client.get("/api/routes/?page=1&page_size=1")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 2)
        self.assertEqual(len(payload["items"]), 1)
        self.assertTrue(payload["pagination"]["has_next"])

    def test_invalid_page_size_returns_structured_error(self):
        response = self.client.get("/api/routes/?page_size=101")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["parameter"], "page_size")

    def test_invalid_sort_returns_structured_error(self):
        response = self.client.get("/api/routes/?sort=price")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "invalid_request")

    def test_write_methods_are_not_allowed(self):
        response = self.client.post("/api/routes/", data={})
        self.assertEqual(response.status_code, 405)
