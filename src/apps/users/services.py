"""
Module provides utility functions for token management and email services for user authentication
and password management.
"""
import jwt
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import AuthenticationFailed

from apps.users.jwt_utils import decode_refresh_token, generate_access_token


def update_access_token(refresh_token):
    """
    Validates the refresh token, extracts the user ID, and generates a new access token.
    """
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationFailed("User identifier not found in JWT")

        access_token = generate_access_token(user_id)

        return access_token

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("Token has expired") from e

    except jwt.InvalidTokenError as e:
        raise AuthenticationFailed("Invalid token") from e


def send_password_reset_email(email, password_forget_url):
    """
    Sends a password reset email to the specified email address.
    """
    subject = "Password Reset Request"
    message = f"Hi, click on the link to reset password:\n{password_forget_url}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
