from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import (
    AuthTokenSerializer,
    PasswordForgetSerializer,
    PasswordResetSerializer,
    RefreshTokenSerializer,
    UserSerializer,
)


class UserRegisterAPI(APIView):
    """
    An endpoint to create a new user.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class TokenRefreshView(APIView):
    """
    An endpoint to refresh JWT access tokens using a refresh token.
    """

    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data.get("refresh_token")
                payload = jwt.decode(
                    refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                user_id = payload["user_id"]

                if user_id is None:
                    raise AuthenticationFailed("User identifier not found in JWT")

                new_access_token = jwt.encode(
                    {"user_id": user_id, "exp": datetime.now() + timedelta(minutes=5)},
                    settings.SECRET_KEY,
                    algorithm="HS256",
                )
                return Response(
                    {"access_token": new_access_token}, status=status.HTTP_200_OK
                )
            except jwt.ExpiredSignatureError:
                return Response(
                    {"error": "Refresh token expired"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            except jwt.InvalidTokenError:
                return Response(
                    {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordForgetView(APIView):
    """
    An endpoint for user to send POST request to reset password.
    """

    serializer_class = PasswordForgetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            reset_token = jwt.encode(
                {"user_id": str(user.id), "exp": datetime.now() + timedelta(minutes=5)},
                settings.SECRET_KEY,
                algorithm="HS256",
            )

            password_forget_url = (
                request.build_absolute_uri(reverse("password-forget"))
                + f"?token={reset_token}"
            )

            # Send email
            subject = "Password Reset Request"
            message = f"Hi, click on the link to reset password:\n{password_forget_url}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return Response(
                "Password reset e-mail has been sent.", status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """
    An endpoint for user to send POST request to make new password
    """

    serializer_class = PasswordResetSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data["reset_token"]
            new_password = serializer.validated_data["new_password"]
            try:
                payload = jwt.decode(
                    reset_token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                user_id = payload["user_id"]
                if user_id is None:
                    raise jwt.InvalidTokenError

                user = get_user_model().objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."},
                    status=status.HTTP_200_OK,
                )

            except jwt.ExpiredSignatureError:
                return Response(
                    {"error": "Reset token has expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except (jwt.InvalidTokenError, get_user_model().DoesNotExist):
                return Response(
                    {"error": "Invalid token or user does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
