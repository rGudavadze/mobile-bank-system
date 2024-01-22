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

    def test_successful_login(self):
        """
        Test successful login.
        """
        response = self.client.post(self.url, self.body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
