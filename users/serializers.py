# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # Add 'password1' field
    password2 = serializers.CharField(write_only=True)  # Add 'password2' field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include password fields
