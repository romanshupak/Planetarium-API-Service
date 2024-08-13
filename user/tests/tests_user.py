from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


USER_URL = reverse("user:create")


class UserSerializerTests(TestCase):
    """Test UserSerializer functionality"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a user"""
        payload = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "is_staff": False
        }
        res = self.client.post(USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.email, payload["email"])
        self.assertFalse(user.is_staff)

    def test_create_user_with_no_password(self):
        """Test creating a user with no password"""
        payload = {
            "email": "testuser@example.com",
        }
        res = self.client.post(USER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)
