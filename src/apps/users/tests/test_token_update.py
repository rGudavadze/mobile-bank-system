"""
Tests for the access token update endpoint.
"""
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.jwt_utils import generate_refresh_token


def generate_expired_refresh_token(user_id):
    """
    Generates an expired JWT refresh token for a given user ID.
    """
    exp = datetime.utcnow() - timedelta(days=1)
    payload = {"user_id": str(user_id), "exp": exp}
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return expired_token


class TokenUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.refresh_token = generate_refresh_token(self.user.id)
        self.expired_refresh_token = generate_expired_refresh_token(self.user.id)
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
        data = {"refresh_token": "invalid_token"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_refresh_token(self):
        """
        Test that an expired token is rejected.
        """
        data = {"refresh_token": self.expired_refresh_token}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
