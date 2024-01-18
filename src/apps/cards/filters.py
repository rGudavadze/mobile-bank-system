import django_filters

from apps.cards.models import Card


class CardFilter(django_filters.FilterSet):
    class Meta:
        model = Card
        fields = ["account"]
