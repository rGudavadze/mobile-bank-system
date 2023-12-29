from models import Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "created_at",
            "profile",
            "account_number",
            "account_type",
            "balance",
            "is_active",
        )
        read_only_fields = ("id", "created_at", "is_active")
