from rest_framework import serializers
from .models import BadThingType, BadThing


class BadThingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadThingType
        fields = ['name']


class BadThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadThing
        fields = ['id', 'type']
