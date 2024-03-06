"""Serializer Module"""

from rest_framework import serializers

from apps.cards.models import Card, Account
from django.contrib.auth.models import User


class CardSerializer(serializers.ModelSerializer):
    """Serializer for Card"""

    class Meta:
        model = Card
        fields = (
            "id",
            "url",
            "account",
            "card_type",
            "card_number",
            "expiration_date",
            "cvc",
            "is_active",
            "created_at",
            "updated_at",
            "deleted",
        )

    def create(self, validated_data):
        # Create a new Card instance, including read-only fields
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Only update the 'is_active' field if it's present in the validated data
        is_active = validated_data.get('is_active')
        if is_active:
            instance.is_active = is_active
            instance.save()
        return instance

    def to_representation(self, instance):
        # Customize the representation to include only 'is_active' during a PUT request
        if self.context['request'].method == 'PUT':
            return {'is_active': instance.is_active}
        return super().to_representation(instance)
