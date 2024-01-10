import jwt
from rest_framework.exceptions import AuthenticationFailed

from apps.users.jwt_utils import decode_refresh_token, generate_access_token


def update_access_token(refresh_token):
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("user_id")

        if user_id is None:
            raise AuthenticationFailed("User identifier not found in JWT")

        access_token = generate_access_token(user_id)

        return access_token

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("Token has expired") from e

    except jwt.InvalidTokenError as e:
        raise AuthenticationFailed("Invalid token") from e
