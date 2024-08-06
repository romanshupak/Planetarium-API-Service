# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from rest_framework import status
#
# from rest_framework.reverse import reverse
# from rest_framework.test import APIClient
#
# from planetarium.models import ShowSession
# from planetarium.serializers import ShowSessionSerializer
#
# SHOW_SESSION_URL = reverse("planetarium:showsession-list")
#
#
# def sample_user(is_staff=False, **params):
#     """Create and return a sample user"""
#     return get_user_model().objects.create_user(**params, is_staff=is_staff)
#
#
# def sample_show_session(**params):
#     defaults = {
#         "astronomy_show": "test show",
#         "planetarium_dome": "test dome",
#         "show_time": "2024-12-06"
#     }
#     defaults.update(params)
#     return ShowSession.objects.create(**defaults)
#
#
# class PublicShowSessionTests(TestCase):
#     """Test unauthenticated API requests"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_auth_required(self):
#         """Test that authentication is required"""
#         res = self.client.get(SHOW_SESSION_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateShowSessionTests(TestCase):
#     """Test authenticated API requests"""
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = sample_user(email="test@test.com", password="testpass")
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_showsessions(self):
#         """Test retrieving a list of ShowSessions"""
#         sample_show_session()
#         sample_show_session(name="Another Session")
#
#         res = self.client.get(SHOW_SESSION_URL)
#
#         show_sessions = ShowSession.objects.all()
#         serializer = ShowSessionSerializer(show_sessions, many=True)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import ShowSession, AstronomyShow, PlanetariumDome
from planetarium.serializers import ShowSessionSerializer, ShowSessionListSerializer

SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def sample_user(is_staff=False, **params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params, is_staff=is_staff)


def sample_astronomy_show(**params):
    """Create and return a sample AstronomyShow"""
    defaults = {
        "title": "Sample Show",
        "description": "Sample Description",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


def sample_planetarium_dome(**params):
    """Create and return a sample PlanetariumDome"""
    defaults = {
        "name": "Sample Dome",
        "rows": 10,
        "seats_in_row": 15,
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show_session(**params):
    """Create and return a sample ShowSession"""
    astronomy_show = sample_astronomy_show()
    planetarium_dome = sample_planetarium_dome()
    defaults = {
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
        "show_time": datetime(2024, 12, 6, 18, 0),
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


class PublicShowSessionTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShowSessionTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user(email="test@test.com", password="testpass")
        self.client.force_authenticate(self.user)

    def test_retrieve_showsessions(self):
        """Test retrieving a list of ShowSessions"""
        sample_show_session()
        sample_show_session(
            astronomy_show=sample_astronomy_show(title="Another Show"),
            planetarium_dome=sample_planetarium_dome(name="Another Dome"),
            show_time=datetime(2024, 12, 7, 18, 0)
        )

        res = self.client.get(SHOW_SESSION_URL)

        show_sessions = ShowSession.objects.all()
        serializer = ShowSessionListSerializer(show_sessions, many=True)

        res_data_sorted = sorted(res.data, key=lambda x: x['id'])
        serializer_data_sorted = sorted(serializer.data, key=lambda x: x['id'])

        for item in res_data_sorted:
            item.pop('tickets_available', None)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data_sorted, serializer_data_sorted)
