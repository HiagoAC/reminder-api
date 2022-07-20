"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'phone_number', 'name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 10},
            'phone_number': {'required': False},
            'name': {'required': False},
            }

    def create(self, validated_data):
        """Create and return an user instance with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)

        return user
