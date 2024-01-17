from django.urls import path

from apps.users.views import (
    PasswordForgetAPIView,
    PasswordResetAPIView,
    TokenRefreshAPIView,
    UserLoginAPIView,
    UserRegisterAPIView,
)

urlpatterns = [
    # Endpoint for user registration
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    # Endpoints for user login and JWT token management
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("token-refresh/", TokenRefreshAPIView.as_view(), name="token-refresh"),
    # Password management endpoints
    path("password-forget/", PasswordForgetAPIView.as_view(), name="password-forget"),
    path("password-reset/", PasswordResetAPIView.as_view(), name="password-reset"),
]
