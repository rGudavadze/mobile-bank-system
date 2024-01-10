import jwt
from django.contrib.auth import get_user_model
from django.urls import reverse
from jwt import InvalidTokenError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.jwt_utils import (
    decode_refresh_token,
    generate_access_token,
    generate_refresh_token,
)
from apps.users.serializers import (
    AuthTokenSerializer,
    PasswordForgetSerializer,
    PasswordResetSerializer,
    RefreshTokenSerializer,
    UserSerializer,
)
from apps.users.services import send_password_reset_email, update_access_token


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
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_200_OK,
        )


class TokenRefreshView(APIView):
    """
    An endpoint to refresh JWT access tokens using a refresh token.
    """

    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            access_token = update_access_token(serializer.data.get("refresh_token"))
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordForgetView(APIView):
    """
    An endpoint for user to send POST request to reset password.
    """

    serializer_class = PasswordForgetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_token = generate_access_token(user.id)

        # Generate password forget url
        password_forget_url = (
            request.build_absolute_uri(reverse("password-forget"))
            + f"?token={reset_token}"
        )

        # Send password reset email
        send_password_reset_email(user, password_forget_url)

        return Response(
            f"Password reset e-mail has been sent. {password_forget_url}",
            status=status.HTTP_200_OK,
        )


class PasswordResetView(APIView):
    """
    An endpoint for user to send PATCH request to make new password.
    """

    serializer_class = PasswordResetSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]
        try:
            payload = decode_refresh_token(reset_token)
            user_id = payload.get("user_id")
            if user_id is None:
                raise InvalidTokenError("Invalid token")

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
