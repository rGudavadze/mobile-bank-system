from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cards.models import Account, Card
from apps.cards.serializers import CardSerializer
from utils.permissions import IsCardDetailOwner, IsCardListOwner

from .filters import CardFilter


class CardListView(generics.ListCreateAPIView):
    permission_classes = [IsCardListOwner]
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filterset_class = CardFilter

    def get_queryset(self):
        account_id = self.request.GET.get("account")

        if account_id:
            queryset = Card.objects.select_related("account").filter(account=account_id)
        else:
            queryset = Card.objects.select_related("account__profile__user").filter(
                account__profile__user=self.request.user
            )

        return queryset

    def create(self, request, *args, **kwargs):
        account_id = request.data.get("account")
        if not Account.objects.filter(id=account_id, profile__user=request.user).exists():
            return Response(
                {"error": "Invalid account for the current user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsCardDetailOwner]
