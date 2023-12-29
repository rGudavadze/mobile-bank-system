from django.db import models

from apps.base.models import BaseModel
from apps.profiles.models import Profile


class AccountTypeChoice(models.TextChoices):
    DEPOSIT = "deposit"
    CREDIT = "credit"
    DEBIT = "debit"
    CONSUMER = "consumer"


class Account(BaseModel):
    """Account model."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(choices=AccountTypeChoice.choices)
    balance = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.account_number
