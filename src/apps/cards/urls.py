from django.urls import path

from apps.cards.views import CardDetailView, CardListView

urlpatterns = [
    path("", CardListView.as_view(), name="card-list"),
    path("<uuid:pk>/", CardDetailView.as_view(), name="card-detail"),
]
