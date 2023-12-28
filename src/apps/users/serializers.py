from models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")
        write_only_fields = ("password",)
