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
    cvc = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.card_number
