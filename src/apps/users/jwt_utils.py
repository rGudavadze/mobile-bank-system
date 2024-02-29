"""
Module provides utility functions for generating and decoding JSON Web Tokens (JWTs)
for user authentication. It includes functions to create both access tokens and
refresh tokens, as well as a function to decode a given refresh token.
"""
from datetime import datetime, timedelta

import jwt
from django.conf import settings


def generate_access_token(user_id):
    """
    Generates a JWT access token with a short expiration time.
    This token is used for user authentication in the application.
    """
    access_token_payload = {
        "user_id": str(user_id),
        "exp": datetime.timestamp(datetime.now() + timedelta(minutes=60)),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


def generate_refresh_token(user_id):
    """
    Generates a JWT refresh token with a longer expiration time.
    This token can be used to renew the access token once it expires.
    """
    refresh_token_payload = {
        "user_id": str(user_id),
        "exp": datetime.timestamp(datetime.now() + timedelta(days=30)),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return refresh_token


def decode_refresh_token(refresh_token):
    """
    Decodes a given refresh token to extract its payload, such as the user ID and expiration timestamp.
    """
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload
