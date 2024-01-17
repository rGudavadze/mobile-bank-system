"""
Module implements the JWTAuthentication class which extends Django's
TokenAuthentication to use JSON Web Tokens (JWT) for user authentication.
It is designed to integrate with Django REST Framework's authentication mechanism.
"""
import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from apps.users.jwt_utils import decode_refresh_token


class JWTAuthentication(TokenAuthentication):
    """
    Extends Django's TokenAuthentication to authenticate users by decoding and verifying JWTs.
    """

    def authenticate(self, request):
        """
        Extracts and decodes the JWT from the request, and
        authenticates the user based on the token's payload.
        """
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        if jwt_token is None:
            return None

        # Decode the JWT and verify its signature
        try:
            payload = decode_refresh_token(jwt_token)
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed("Invalid signature")
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token")

        # Get the user from the database
        user_id = payload.get("user_id")
        if user_id is None:
            raise exceptions.AuthenticationFailed("User identifier not found in JWT")

        user = get_user_model().objects.get(id=user_id)
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return user, payload
