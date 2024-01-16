from django.urls import path

from apps.transactions.views import (
    CreateTransactionView,
    RetrieveTransactionView,
)

urlpatterns = [
    path(
        "transactions/",
        CreateTransactionView.as_view(),
        name="list_create_transaction",
    ),
    path(
        "transactions/<uuid:id>",
        RetrieveTransactionView.as_view(),
        name="get_transaction",
    ),
]
