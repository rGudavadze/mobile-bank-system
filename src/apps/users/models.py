from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.base.models import BaseModel
from apps.users.managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()
