from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from apps.base.models import BaseModel


# Create your models here.
class User(BaseModel, AbstractBaseUser):
    email = models.EmailField()

    USERNAME_FIELD = "email"


