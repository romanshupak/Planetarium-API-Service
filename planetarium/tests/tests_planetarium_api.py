from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer
)

PLANETARIUM_URL = reverse("planetarium:astronomyshow-list")


def detail_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomyshow-detail",
        args=(astronomy_show_id,)
    )


def sample_astronomy_show(**params) -> AstronomyShow:
    defaults = {
        "title": "test title",
        "description": "test description",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


class UnauthenticatedPlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.test",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_shows_list(self):
        sample_astronomy_show()
        sample_astronomy_show(
            title="test title",
            description="Another Test Description"
        )

        res = self.client.get(PLANETARIUM_URL)

        astronomy_shows = AstronomyShow.objects.order_by("id")
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for res_item, serializer_item in zip(res.data, serializer.data):
            self.assertEqual(res_item, serializer_item)

    def test_filter_astronomy_shows_by_themes(self):
        theme1 = ShowTheme.objects.create(name="Theme 1")
        theme2 = ShowTheme.objects.create(name="Theme 2")

        astronomy_show1 = sample_astronomy_show(title="Astronomy Show 1")
        astronomy_show2 = sample_astronomy_show(title="Astronomy Show 2")

        astronomy_show1.themes.add(theme1)
        astronomy_show2.themes.add(theme2)

        astronomy_show3 = sample_astronomy_show(title="Astronomy Show without themes")

        res = self.client.get(
            PLANETARIUM_URL, {"themes": f"{theme1.id},{theme2.id}"}
        )

        serializer1 = AstronomyShowListSerializer(astronomy_show1)
        serializer2 = AstronomyShowListSerializer(astronomy_show2)
        serializer3 = AstronomyShowListSerializer(astronomy_show3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_astronomy_shows_by_titles(self):
        astronomy_show1 = sample_astronomy_show(title="Stars")
        astronomy_show2 = sample_astronomy_show(title="Moon")
        astronomy_show3 = sample_astronomy_show(title="No match")

        res = self.client.get(PLANETARIUM_URL, {"title": "Stars"})

        serializer1 = AstronomyShowListSerializer(astronomy_show1)
        serializer2 = AstronomyShowListSerializer(astronomy_show2)
        serializer3 = AstronomyShowListSerializer(astronomy_show3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_astronomy_show_detail(self):
        astronomy_show = sample_astronomy_show()
        astronomy_show.themes.add(ShowTheme.objects.create(name="ShowTheme"))
        astronomy_show.themes.add(ShowTheme.objects.create(name="Moon"))

        url = detail_url(astronomy_show.id)

        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(astronomy_show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "Test Title",
            "description": "Test Description"
        }
        res = self.client.post(PLANETARIUM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.test",
            "testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        payload = {
            "title": "Test Title",
            "description": "Test Description"
        }
        res = self.client.post(PLANETARIUM_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(astronomy_show, key))

    def test_create_astronomy_show_with_themes(self):
        theme1 = ShowTheme.objects.create(name="Theme 1")
        theme2 = ShowTheme.objects.create(name="Theme 2")

        payload = {
            "title": "Test Title",
            "description": "Test Description",
            "themes": [theme1.id, theme2.id]
        }
        res = self.client.post(PLANETARIUM_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])
        themes = astronomy_show.themes.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(theme1, themes)
        self.assertIn(theme2, themes)
        self.assertEqual(themes.count(), 2)

    def test_delete_astronomy_show_not_allowed(self):
        astronomy_show = sample_astronomy_show()

        url = detail_url(astronomy_show.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



