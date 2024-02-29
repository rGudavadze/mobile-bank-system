"""
Tests for the update access token method.
"""
from unittest.mock import patch

from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase

from apps.users.services import update_access_token


class UpdateAccessTokenTestCase(APITestCase):
    @patch("apps.users.services.decode_refresh_token")
    @patch("apps.users.services.generate_access_token")
    def test_update_access_token_success(
        self, mocked_generate_access_token, mocked_decoded_payload
    ):
        """
        Test the update access token successfully.
        """

        mocked_decoded_payload.return_value = {"user_id": "mocked_user_id"}
        mocked_generate_access_token.return_value = "mocked_access_token"

        result_access_token = update_access_token("dummy_refresh_token")

        self.assertEqual(result_access_token, "mocked_access_token")

        mocked_decoded_payload.assert_called_once_with("dummy_refresh_token")
        mocked_generate_access_token.assert_called_once_with("mocked_user_id")

    @patch("apps.users.services.decode_refresh_token")
    def test_update_access_token_with_invalid_refresh_token(self, mocked_decoded_payload):
        """
        Test InvalidTokenError exception is raised if token is invalid.
        """

        mocked_decoded_payload.side_effect = InvalidTokenError("Invalid token")

        with self.assertRaises(AuthenticationFailed) as context:
            update_access_token("dummy_refresh_token")

        self.assertIn("Invalid token", str(context.exception))

    @patch("apps.users.services.decode_refresh_token")
    def test_update_access_token_with_expired_refresh_token(self, mocked_decoded_payload):
        """
        Test ExpiredSignatureError exception is raised if token is expired.
        """

        mocked_decoded_payload.side_effect = ExpiredSignatureError("Token has expired")

        with self.assertRaises(AuthenticationFailed) as context:
            update_access_token("dummy_refresh_token")

        self.assertIn("Token has expired", str(context.exception))

    @patch("apps.users.services.decode_refresh_token")
    def test_update_access_token_missing_user_id_in_payload(self, mocked_decoded_payload):
        """
        Test AuthenticationFailed exception is raised if user identifier is not found in JWT payload.
        """

        mocked_decoded_payload.return_value = {}

        with self.assertRaises(AuthenticationFailed) as context:
            update_access_token("dummy_refresh_token")

        self.assertIn("User identifier not found in JWT", str(context.exception))
