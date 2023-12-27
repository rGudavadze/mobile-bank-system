from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "user",
            "birth_date",
            "address",
        )
        read_only_fields = ("id",)
