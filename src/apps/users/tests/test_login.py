"""
Tests for the user login endpoint.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="email@gmail.com", password="password"
        )
        self.url = reverse("user-login")
        self.body = dict(email="email@gmail.com", password="password")

    def test_login_successful(self):
        """
        Test successful login.
        """
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_incorrect_email(self):
        """
        Test login with incorrect email address.
        """
        self.body.update(email="incorrect@gmail.com")
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("non_field_errors")[0], "Unable to log in.")

    def test_login_incorrect_password(self):
        """
        Test login with incorrect password.
        """
        self.body.update(password="incorrect_password")
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("non_field_errors")[0], "Unable to log in.")
