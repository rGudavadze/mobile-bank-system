from django.db import models

from apps.account.models import Account
from apps.base.models import BaseModel


class TransactionStatusChoice(models.TextChoices):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ERROR = "ERROR"


class TransactionTypeChoice(models.TextChoices):
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class Transaction(BaseModel):
    """Model for Transactions"""

    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="received_transactions"
    )
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(choices=TransactionStatusChoice.choices)
    type = models.CharField(choices=TransactionTypeChoice.choices)

    def __str__(self):
        return self.id
