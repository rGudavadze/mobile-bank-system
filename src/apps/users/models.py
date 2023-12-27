from django.contrib.auth.models import AbstractUser

from apps.base.models import BaseModel


# Create your models here.
class User(BaseModel, AbstractUser):
    pass
