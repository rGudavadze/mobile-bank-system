from rest_framework import serializers

from .models import Account


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
        read_only_fields = ("id", "balance", "created_at", "is_active")
