from django_filters import rest_framework as filters

from apps.cards.models import Card


class CardFilter(filters.FilterSet):
    account = filters.CharFilter(field_name="account")

    class Meta:
        model = Card
        fields = ("account",)
