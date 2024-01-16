from django.urls import path

from apps.cards.views import CardDetailView, CardListView

urlpatterns = [
    path("cards/", CardListView.as_view(), name="card-list"),
    path("cards/<uuid:pk>/", CardDetailView.as_view(), name="card-detail"),
]
