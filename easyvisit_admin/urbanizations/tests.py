from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Urbanization, Plan  # Asegúrate de ajustar la ubicación real de tu modelo


class UrbanizationViewPostTest(TestCase):
    def setUp(self):
        # Crear un objeto de Plan con pk = 1
        self.plan = Plan.objects.create(pk=1, name="Plan Name", price=10.0)
        self.client = APIClient()

    def test_create_urbanization(self):
        urbanization_data = {
            "name": "Sample Urbanization",
            "street": "Main Street",
            "number": "123",
            "neighborhood": "Downtown",
            "city": "Cityville",
            "state": "Stateville",
            "country": "Countryland",
            "zip_code": 12345,
            "houses": 100,
            "is_active": True,
            "rfc": "XXXX000000X00",
            "email": "sample@example.com",
            "plan": 1
        }

        response = self.client.post("/urbanization", urbanization_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        Urbanization.objects.all().delete()
