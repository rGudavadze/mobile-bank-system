"""
Tests for the access token update endpoint.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.jwt_utils import generate_refresh_token


class TokenUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.refresh_token = generate_refresh_token(self.user)
        self.url = reverse("token-update")

    def test_successful_token_update(self):
        """
        Test successful access token update.
        """
        data = {"refresh_token": self.refresh_token}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)

    def test_invalid_refresh_token(self):
        """
        Test that an invalid refresh token is rejected.
        """
        pass

    def test_expired_token_refresh(self):
        """
        Test that an expired token is
        """
        pass
