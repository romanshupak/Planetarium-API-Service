import pytz
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import (
    Reservation,
    Ticket,
    ShowSession,
    AstronomyShow,
    PlanetariumDome
)

RESERVATION_URL = reverse("planetarium:reservation-list")


def sample_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


def sample_planetarium_dome(**params):
    defaults = {
        "name": "Sample Dome",
        "rows": 10,
        "seats_in_row": 15
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample Show",
        "description": "A sample description",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


def sample_show_session(**params):
    astronomy_show = sample_astronomy_show()
    planetarium_dome = sample_planetarium_dome()
    show_time = datetime(2024, 12, 6, 18, 0, 0, tzinfo=pytz.UTC)
    defaults = {
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
        "show_time": show_time,
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def sample_reservation(user, **params):
    defaults = {
        "user": user,
    }
    defaults.update(params)
    return Reservation.objects.create(**defaults)


def sample_ticket(reservation, show_session, **params):
    defaults = {
        "row": 1,
        "seat": 1,
        "show_session": show_session,
        "reservation": reservation,
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)


class PublicReservationTests(TestCase):
    """Test the publicly available reservation API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReservationTests(TestCase):
    """Test the private reservation API"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user(email="test@test.com", password="testpass")
        self.client.force_authenticate(self.user)

    def test_create_reservation(self):
        """Test creating a reservation with tickets"""
        show_session = sample_show_session()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": show_session.id},
                {"row": 1, "seat": 2, "show_session": show_session.id},
            ]
        }

        res = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(id=res.data['id'])
        self.assertEqual(reservation.tickets.count(), 2)

    def test_create_reservation_with_invalid_ticket(self):
        """Test creating a reservation with invalid ticket data"""
        show_session = sample_show_session()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": show_session.id},
                {"row": 1, "seat": 100, "show_session": show_session.id},
            ]
        }

        res = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_list_reservations(self):
        """Test retrieving a list of reservations"""
        show_session = sample_show_session()
        reservation1 = sample_reservation(user=self.user)
        sample_ticket(reservation=reservation1, show_session=show_session, row=1, seat=1)
        sample_ticket(reservation=reservation1, show_session=show_session, row=1, seat=2)

        reservation2 = sample_reservation(user=self.user)
        sample_ticket(reservation=reservation2, show_session=show_session, row=2, seat=1)

        res = self.client.get(RESERVATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertIn('id', res.data['results'][0])
        self.assertIn('tickets', res.data['results'][0])
        self.assertEqual(len(res.data['results'][0]['tickets']), 2)
        self.assertEqual(len(res.data['results'][1]['tickets']), 1)