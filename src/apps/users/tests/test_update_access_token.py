"""
Tests for the update access token method.
"""
from unittest.mock import patch

from rest_framework.test import APITestCase

from apps.users.services import update_access_token


class UpdateAccessTokenTestCase(APITestCase):
    def setUp(self):
        pass

    @patch("apps.users.jwt_utils.decode_refresh_token")
    @patch("apps.users.jwt_utils.generate_access_token")
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
