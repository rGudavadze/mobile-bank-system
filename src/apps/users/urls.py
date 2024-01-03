from django.urls import path

from apps.users import views

urlpatterns = [path("register/", views.UserRegisterAPI.as_view(), name="user_register")]
