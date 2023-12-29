from rest_framework import generics

from .models import Account
from .serializers import AccountSerializer


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
