"""
Test the JWT access and refresh tokens generation and decoding functionality.
"""
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory
from apps.users.jwt_utils import (
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)


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

    def test_generate_and_decode_access_token_success(self):
        """
        Integration test for generating and decoding a JWT access token
        to ensure the token contains the correct payload and is valid.
        """

        access_token = generate_access_token(self.user.id)
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

        # Verify the payload contents
        self.assertEqual(payload["user_id"], str(self.user.id))

        # Verify the expiration time is approximately 60 minutes from now
        exp = datetime.fromtimestamp(payload["exp"])
        self.assertTrue(
            timedelta(minutes=59) < exp - datetime.now() < timedelta(minutes=61)
        )

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

    def test_generate_and_decode_refresh_token_success(self):
        """
        Integration test for generating and decoding a JWT refresh token
        to ensure the token contains the correct payload and is valid.
        """

        refresh_token = generate_refresh_token(self.user.id)
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

        # Verify the payload contents
        self.assertEqual(payload["user_id"], str(self.user.id))

        # Verify the expiration time is approximately 30 days from now
        exp = datetime.fromtimestamp(payload["exp"])
        self.assertTrue(timedelta(days=29) < exp - datetime.now() < timedelta(days=31))

    @patch("apps.users.jwt_utils.jwt.decode")
    @patch("apps.users.jwt_utils.datetime")
    def test_decode_refresh_token_success(self, mock_datetime, mock_jwt_decode):
        """
        Test the JWT refresh token decode method.
        """

        exp = mock_datetime.timestamp.return_value = self.fixed_now + timedelta(days=30)
        mock_payload = {"user_id": str(self.user.id), "exp": exp}

        mock_jwt_decode.return_value = mock_payload

        decoded_payload = decode_refresh_token("mocked_refresh_token")

        mock_jwt_decode.assert_called_once_with(
            "mocked_refresh_token", settings.SECRET_KEY, algorithms=["HS256"]
        )
        self.assertEqual(decoded_payload, mock_payload)

    @patch("apps.users.jwt_utils.jwt.decode")
    def test_decode_refresh_token_expired(self, mock_jwt_decode):
        """
        Test the expired JWT refresh token method.
        """

        mock_jwt_decode.side_effect = ExpiredSignatureError("Token is expired")

        with self.assertRaises(ExpiredSignatureError):
            decode_refresh_token("mocked_refresh_token")

        mock_jwt_decode.assert_called_once_with(
            "mocked_refresh_token", settings.SECRET_KEY, algorithms=["HS256"]
        )

    @patch("apps.users.jwt_utils.jwt.decode")
    def test_decode_refresh_token_invalid(self, mock_jwt_decode):
        """
        Test the invalid JWT refresh token method.
        """

        mock_jwt_decode.side_effect = InvalidTokenError("Invalid token")

        with self.assertRaises(InvalidTokenError):
            decode_refresh_token("mocked_refresh_token")

        mock_jwt_decode.assert_called_once_with(
            "mocked_refresh_token", settings.SECRET_KEY, algorithms=["HS256"]
        )
