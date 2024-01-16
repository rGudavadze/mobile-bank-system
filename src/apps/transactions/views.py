"""Views for the transactions app."""
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    get_object_or_404,
)

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer


class CreateTransactionView(ListCreateAPIView):
    """Create a new transaction."""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(sender__profile__user=user)


class RetrieveTransactionView(RetrieveAPIView):
    """Retrieve a transaction."""

    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.all()  # You can adjust this if needed

    def get_object(self):
        transaction_id = self.kwargs.get("id")
        return get_object_or_404(Transaction, id=transaction_id)
