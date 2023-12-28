"""card model."""
from django.db import models

from apps.account.models import Account
from apps.base.models import BaseModel


class CardTypeChoice(models.TextChoices):
    CREDIT = "credit"
    DEBIT = "debit"


class Card(BaseModel):
    """Card model."""

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_type = models.CharField(choices=CardTypeChoice.choices)
    card_number = models.CharField(max_length=255)
    expiration_date = models.DateField()
    cvc = models.IntegerField(max_length=3)
    is_active = models.BooleanField(default=True)
