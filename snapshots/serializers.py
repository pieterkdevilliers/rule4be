from rest_framework import serializers
from rule4be.serializers import UserNameField
from .models import AreaOfLife, Snapshot

class AOLSerializer(serializers.Serializer):
    """
    Serializes an AOL object.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return AreaOfLife.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class SnapshotSerializer(serializers.Serializer):
    """
    Serializes a Snapshot object.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    area_of_life = serializers.PrimaryKeyRelatedField(queryset=AreaOfLife.objects.all())
    body = serializers.CharField(max_length=500)
    created = serializers.DateField(read_only=True)
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_video(self, obj):
        return obj.video.url if obj.video else None

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return Snapshot.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.area_of_life = validated_data.get('area_of_life', instance.area_of_life)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


# class SnapshotSerializer(serializers.Serializer):
#     """
#     Serializes a Snapshot object.
#     """
#     owner = serializers.ReadOnlyField(source='owner.username')
#     area_of_life = serializers.PrimaryKeyRelatedField(queryset=AreaOfLife.objects.all())
#     body = serializers.CharField(max_length=500)
#     created = serializers.DateField(read_only=True)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         validated_data['owner'] = user
#         return Snapshot.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.area_of_life = validated_data.get('area_of_life', instance.area_of_life)
#         instance.body = validated_data.get('body', instance.body)
#         instance.save()
#         return instance

