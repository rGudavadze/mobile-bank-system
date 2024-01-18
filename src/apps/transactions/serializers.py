"""Serializers for the transactions model."""
from rest_framework import serializers

from apps.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction model."""
    class Meta:
        model = Transaction
        fields = ('id', 'sender', 'receiver', 'amount', 'status', 'type')
        read_only_fields = ('id', 'status')
