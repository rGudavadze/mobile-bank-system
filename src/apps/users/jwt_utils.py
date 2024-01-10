from datetime import datetime, timedelta

import jwt
from django.conf import settings


def generate_access_token(user_id):
    access_token_payload = {
        "user_id": str(user_id),
        "exp": datetime.timestamp(datetime.now() + timedelta(minutes=5)),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


def generate_refresh_token(user_id):
    refresh_token_payload = {
        "user_id": str(user_id),
        "exp": datetime.timestamp(datetime.now() + timedelta(minutes=30)),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return refresh_token


def decode_refresh_token(refresh_token):
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload
