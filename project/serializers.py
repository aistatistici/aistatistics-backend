import serpy
from datetime import datetime

from rest_framework import serializers


from .models import Project


class ProjectSerializer(serpy.Serializer):

    id = serpy.Field()
    name = serpy.Field()
    description = serpy.Field()
    last_update = serpy.Field()
    created_at = serpy.Field()


class PostProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'description')

    def update(self, instance, validated_data):
        instance.last_update = datetime.now()
        instance.save()
        return instance

