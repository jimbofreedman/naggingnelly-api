from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import BadThing, BadThingType


class BadThingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadThingType
        fields = ['id', 'name']


class BadThingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if (validated_data["owner"] != validated_data["type"].owner):
            raise ValidationError("Unknown BadThingType")

        return BadThing.objects.create(**validated_data)

    class Meta:
        model = BadThing
        fields = ['id', 'type']
