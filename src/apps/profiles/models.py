from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel


class Profile(BaseModel):
    """
    User profile model
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()
    address = models.TextField()
    mobile_number = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
