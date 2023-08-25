from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class UserNameField(serializers.Field):
    def to_representation(self, value):
        return value.username
    
class CurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self):
        return self.user.username