"""
Serializers for the user API View.
These basically convert model instances to and from python datatypes which can then be converted to json.
The view for creatng a user will use this serializer.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user instance object."""

    class Meta: # specify the model for this serializer, the fields provided
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # this overrides the create method inherited with the create_user method we wrote in our model.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)