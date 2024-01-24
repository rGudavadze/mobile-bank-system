from rest_framework import filters

from apps.cards.models import Card


class CardFilter(filters.FilterSet):
    account = filters.CharFilter(field_name="account")

    class Meta:
        model = Card
        fields = ("account",)
