from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from apps.cards.models import Account, Card
from apps.cards.serializers import CardSerializer

from .filters import CardFilter


class CardListView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filterset_class = CardFilter

    def get_queryset(self):
        account_id = self.request.GET.get("account")

        if account_id:
            queryset = Card.objects.select_related("account").filter(
                account__profile__user=self.request.user, account=account_id
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
    serializer_class = CardSerializer

    def get_object(self):
        return get_object_or_404(
            Card.objects.filter(
                account__profile__user=self.request.user,
            ),
            pk=self.kwargs.get("pk"),
        )
