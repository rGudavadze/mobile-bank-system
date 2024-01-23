"""
Module contains the UserFactory class, a factory for creating mock user instances in Django applications.
"""
import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """
    Factory class for generating mock User instances in Django applications using factory_boy.
    """

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_staff = False
    is_superuser = False
