from rest_framework import serializers
from .models import Action

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'short_description', 'status']
