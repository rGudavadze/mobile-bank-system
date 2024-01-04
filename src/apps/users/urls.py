from django.urls import path

from apps.users import views
from apps.users.views import TokenObtainView, TokenRefreshView

urlpatterns = [
    path("user/register/", views.UserRegisterAPI.as_view(), name="user_register"),
    path("token/", TokenObtainView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
