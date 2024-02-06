"""
Tests for sending password reset email method.
"""
from unittest.mock import patch

from django.conf import settings
from rest_framework.test import APITestCase

from apps.users.services import send_password_reset_email


class SendPasswordResetEmailTestCase(APITestCase):
    def setUp(self):
        pass

    @patch("apps.users.services.send_mail")
    def test_send_password_reset_email_success(self, mock_send_email):
        """
        Test sending password reset email method with success.
        """
        email = "user@example.com"
        password_forget_url = "http://example.com/reset-password/token123"

        send_password_reset_email(email, password_forget_url)

        mock_send_email.assert_called_once_with(
            "Password Reset Request",
            f"Hi, click on the link to reset password:\n{password_forget_url}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
