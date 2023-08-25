from rest_framework import serializers
from rule4be.serializers import UserNameField
from .models import Snapshot, AreaOfLife

class AOLSerializer(serializers.Serializer):
    """
    Serializes an AOL object.
    """
    owner = UserNameField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    


class SnapshotSerializer(serializers.Serializer):
    """
    Serializes a Snapshot object.
    """
    owner = UserNameField(read_only=True)
    area_of_life = AOLSerializer(read_only=True)
    body = serializers.CharField(max_length=500)
    created = serializers.DateField(read_only=True)
