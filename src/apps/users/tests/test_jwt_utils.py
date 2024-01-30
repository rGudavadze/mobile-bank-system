"""
Test the JWT access and refresh tokens generation and decoding functionality.
"""
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from django.conf import settings
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.jwt_utils import generate_access_token, generate_refresh_token


class JWTUtilsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.fixed_now = datetime(2023, 1, 1, 12, 0, 0)

    @patch("apps.users.jwt_utils.jwt.encode")
    @patch("apps.users.jwt_utils.datetime")
    def test_generate_access_token_success(self, mock_datetime, mock_jwt_encode):
        """
        Test the JWT access token successful generation.
        """

        mock_jwt_encode.return_value = "mocked_access_token"
        exp = mock_datetime.timestamp.return_value = self.fixed_now + timedelta(
            minutes=60
        )

        access_token = generate_access_token(self.user.id)

        access_token_payload = {"user_id": str(self.user.id), "exp": exp}

        jwt.encode.assert_called_once_with(
            access_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        self.assertEqual(access_token, "mocked_access_token")

    @patch("apps.users.jwt_utils.jwt.encode")
    @patch("apps.users.jwt_utils.datetime")
    def test_generate_refresh_token_success(self, mock_datetime, mock_jwt_encode):
        """
        Test the JWT refresh token successful generation.
        """

        mock_jwt_encode.return_value = "mocked_refresh_token"
        exp = mock_datetime.timestamp.return_value = self.fixed_now + timedelta(days=30)

        refresh_token = generate_refresh_token(self.user.id)

        refresh_token_payload = {"user_id": str(self.user.id), "exp": exp}

        jwt.encode.assert_called_once_with(
            refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        self.assertEqual(refresh_token, "mocked_refresh_token")
