from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.serializers import ValidationError

from apps.account.models import Account
from apps.account.permissions import IsAccountOwner
from apps.account.serializers import AccountSerializer
from apps.profiles.models import Profile


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user

        return Account.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            raise ValidationError(code=404, detail="User Profile Does Not Exist")
        serializer.save(profile=profile)


class AccountDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAccountOwner]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
