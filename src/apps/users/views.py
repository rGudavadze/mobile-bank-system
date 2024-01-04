from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import AuthTokenSerializer, UserSerializer


class UserRegisterAPI(APIView):
    """
    An endpoint to create a new user.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
    """
    An endpoint to obtain JWT access and refresh tokens for a user.
    """

    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            access_token = jwt.encode(
                {"user_id": str(user.id), "exp": datetime.now() + timedelta(minutes=5)},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            refresh_token = jwt.encode(
                {"user_id": str(user.id), "exp": datetime.now() + timedelta(days=1)},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
