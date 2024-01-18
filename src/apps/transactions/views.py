"""Views for the transactions app."""
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer


class CreateTransactionView(ListCreateAPIView):
    """Create a new transaction."""

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(sender__profile__user=user).select_related(
            "sender__profile__user"
        )


class RetrieveTransactionView(RetrieveAPIView):
    """Retrieve a transaction."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
