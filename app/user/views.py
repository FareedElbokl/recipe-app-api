"""
Views for the user api
"""
from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # The CreateAPIView handles the post req mechanism. We just need to define the serializer
    # The serializer will defines which model we want to create the object instance in
    serializer_class = UserSerializer
