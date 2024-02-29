"""
Tests for the register endpoint.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory


class UserRegisterTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(email="userexists@gmail.com")
        self.url = reverse("user-register")
        self.body = dict(email="unique_email@gmail.com", password="password")

    def test_successful_registration(self):
        """
        Test successful user registration with valid data.
        """
        response = self.client.post(
            self.url,
            self.body,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), "unique_email@gmail.com")

        # Check if user actually created in database
        user = get_user_model()
        self.assertTrue(user.objects.filter(email=self.body.get("email")).exists())

    def test_register_existing_email(self):
        """
        Test user registration with an email that already exists.
        """
        self.body.update(email="userexists@gmail.com")
        response = self.client.post(
            self.url,
            data=self.body,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("email")[0], "user with this email already exists."
        )

    def test_register_invalid_email(self):
        """
        Test user registration with invalid email format.
        """
        self.body.update(email="email")
        response = self.client.post(
            self.url,
            data=self.body,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("email")[0], "Enter a valid email address.")

    def test_access_without_authentication(self):
        """
        Test that the endpoint is accessed without authentication.
        """
        self.client.logout()
        response = self.client.post(self.url, self.body)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
