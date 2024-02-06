"""
Tests for the password forget serializer.
"""

from rest_framework.test import APITestCase

from apps.users.serializers import PasswordForgetSerializer


class PasswordForgetSerializerTestCase(APITestCase):
    def test_valid_email(self):
        """Test serializer with a valid email."""
        valid_data = {"email": "user@example.com"}
        serializer = PasswordForgetSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test serializer with an invalid email format."""
        invalid_data = {"email": "invalid-email"}
        serializer = PasswordForgetSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)  # Ensures error is for 'email' field

    def test_empty_email_field(self):
        """Test serializer with an empty email field."""
        empty_data = {"email": ""}
        serializer = PasswordForgetSerializer(data=empty_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)  # Ensures error is for 'email' field
