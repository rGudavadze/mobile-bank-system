from django.urls import path

from apps.users import views
from apps.users.views import (
    PasswordForgetView,
    PasswordResetView,
    TokenObtainView,
    TokenRefreshView,
)

urlpatterns = [
    # Endpoint for user registration
    path("user/register/", views.UserRegisterAPI.as_view(), name="user-register"),
    # Endpoints for JWT token management
    path("token/", TokenObtainView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # Password management endpoints
    path("user/password-forget/", PasswordForgetView.as_view(), name="password-forget"),
    path("user/password-reset/", PasswordResetView.as_view(), name="password-reset"),
]
