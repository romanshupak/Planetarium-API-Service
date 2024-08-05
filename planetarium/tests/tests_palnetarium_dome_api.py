import os
from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Planetarium_API_Service.settings")

PLANETARIUM_DOME_URL = reverse("planetarium:planetariumdome-list")


def sample_user(is_staff=False, **params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params, is_staff=is_staff)


def sample_planetarium_dome(**params) -> PlanetariumDome:
    defaults = {
        "name": "test name",
        "rows": 10,
        "seats_in_row": 15
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


class PublicPlanetariumDomeApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlanetariumDomeApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user(email="test@test.com", password="testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_planetarium_domes(self):
        """Test retrieving a list of PlanetariumDomes"""
        sample_planetarium_dome()
        sample_planetarium_dome(name="Another Dome")

        res = self.client.get(PLANETARIUM_DOME_URL)

        planetarium_domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(planetarium_domes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
