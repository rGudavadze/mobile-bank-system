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
        self.body = {"email": "unique_email@gmail.com", "password": "password"}

    def test_register_correct(self):
        """
        Test that creating a user is successful.
        """

        response = self.client.post(
            self.url,
            self.body,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Asserting that the response data contains the correct email
        self.assertEqual(response.data.get("email"), "unique_email@gmail.com")

        # Check if user actually created in database
        user = get_user_model()
        self.assertTrue(user.objects.filter(email=self.body.get("email")).exists())

    def test_register_existing_email(self):
        """
        Test that checking if the email already exists.
        """
        self.body.update(email="userexists@gmail.com")
        response = self.client.post(
            self.url,
            data=self.body,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Asserting that the first error message is the expected error message
        self.assertEqual(
            response.data.get("email")[0], "user with this email already exists."
        )
