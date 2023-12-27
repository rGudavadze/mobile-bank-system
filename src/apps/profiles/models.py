from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    """
    User profile model
    """
    user_id = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.TextField()
    mobile_number = models.IntegerField()

    def __str__(self):
        return 'f{self.name}, {self.last_name}, {self.email}, {self.birth_date}, {self.address}, {self.mobile_number}'
