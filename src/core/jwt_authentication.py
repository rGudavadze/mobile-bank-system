import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from apps.users.jwt_utils import decode_refresh_token


class JWTAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        print(jwt_token)
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

        user = get_user_model().objects.filter(id=user_id).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        return user, payload
