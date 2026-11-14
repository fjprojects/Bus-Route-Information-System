from django.test import TestCase
from api.models import ExerciseReference, Measurement, Route


class RouteApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Route.objects.create(
            id="blue-line", name="Blue Line", origin="Central Station",
            destination="Tech Park", stops=["Central Station", "University", "Tech Park"],
            duration_min=22, frequency_min=12,
        )
        Route.objects.create(
            id="green-line", name="Green Line", origin="Central Station",
            destination="University", stops=["Central Station", "Museum", "University"],
            duration_min=16, frequency_min=15,
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

    def test_intermediate_stop_search(self):
        response = self.client.get("/api/routes/?q=Museum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()["items"]], ["green-line"])


class PortfolioDemoApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ExerciseReference.objects.create(
            id="ankle-mobility", name="Ankle mobility",
            category="Gentle ankle movement", description="Illustrative reference.",
            professional_note="Only under qualified professional guidance.",
        )
        Measurement.objects.create(
            date="Sample 01", left_step_time="0.600", right_step_time="0.620",
            walking_speed="0.780", balance_score="76.00",
        )

    def test_exercise_catalogue_endpoint(self):
        response = self.client.get("/api/exercises/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], "AI Recovery Assistant")
        self.assertEqual(response.json()["items"][0]["id"], "ankle-mobility")
        self.assertIn("professional_note", response.json()["items"][0])

    def test_measurement_endpoint_returns_numeric_values(self):
        response = self.client.get("/api/measurements/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["project"], "GaitGuardian")
        self.assertIsInstance(response.json()["items"][0]["walking_speed"], float)

    def test_measurements_endpoint_rejects_post(self):
        response = self.client.post("/api/measurements/", data={})
        self.assertEqual(response.status_code, 405)
