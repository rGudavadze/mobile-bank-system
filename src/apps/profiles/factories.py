"""
Module contains the ProfileFactory class, a factory for creating mock profile instances in Django applications.
"""
import factory
from factory.django import DjangoModelFactory

from apps.profiles.models import Profile
from apps.users.factories import UserFactory


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth")
    address = factory.Faker("address")
    mobile_number = factory.Faker("phone_number")
