from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)
