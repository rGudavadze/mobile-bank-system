import random

from rest_framework import serializers
from schwifty import IBAN

from apps.account.models import Account

COUNTRY_CODE = "GE"
BANK_CODE = "RB"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "created_at",
            "account_number",
            "account_type",
            "balance",
            "is_active",
        )
        read_only_fields = ("id", "balance", "created_at", "is_active", "account_number")

    def create(self, validated_data):
        # Generate a unique IBAN as the account number
        validated_data["account_number"] = self._generate_unique_iban()
        return super().create(validated_data)

    @staticmethod
    def _generate_unique_iban():
        while True:
            random_account_code = random.randint(0000000000000000, 9999999999999999)
            # Generate a random IBAN
            random_iban = IBAN.generate(
                country_code=COUNTRY_CODE,
                bank_code=BANK_CODE,
                account_code=str(random_account_code),
            )

            # Check if the generated IBAN is unique
            if not Account.objects.filter(account_number=random_iban).exists():
                return random_iban
