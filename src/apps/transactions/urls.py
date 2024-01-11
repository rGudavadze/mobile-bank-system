from django.urls import path
from apps.transactions.views import CreateTransactionView, RetrieveTransactionView, ListTransactionView

urlpatterns = [
    path('transactions/', CreateTransactionView.as_view(), name='create_transaction',),
    path('transactions/<uuid:id>', RetrieveTransactionView.as_view(), name='retrive_transaction', ),
    path('transactions/', ListTransactionView.as_view(), name='list_transaction', ),

]