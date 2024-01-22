from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cards.models import Account, Card
from apps.cards.serializers import CardSerializer
from utils.permissions import IsCardOwner

from .filters import CardFilter


class CardListView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsCardOwner]
    filterset_class = CardFilter

    def get_queryset(self):
        account_id = self.request.GET.get("account")

        if account_id is not None:
            queryset = Card.objects.select_related("account").filter(
                account__id=account_id
            )
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
    permission_classes = [IsAuthenticated, IsCardOwner]
