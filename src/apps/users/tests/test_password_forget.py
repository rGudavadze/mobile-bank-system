"""
Tests for the password forget endpoint.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory


class PasswordForgetTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("password-forget")
        self.body = dict(email=self.user.email)

    def test_password_forget_success(self):
        """
        Test successful password forget.
        """
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_forget_with_incorrect_email(self):
        """
        Test password forget with incorrect email address.
        """
        self.body.update(email="incorrect@gmail.com")
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("error"), "User with this email does not exist"
        )

    def generate_access_token_successful(self):
        pass

    def password_forget_url_successful(self):
        pass

    def send_password_reset_email_successful(self):
        pass
