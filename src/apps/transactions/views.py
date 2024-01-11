"""Views for the transactions app."""
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer


class CreateTransactionView(CreateAPIView):
    """Create a new transaction."""
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class RetrieveTransactionView(RetrieveAPIView):
    """Retrieve a transaction."""
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class ListTransactionView(ListAPIView):
    """List all transactions."""
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
