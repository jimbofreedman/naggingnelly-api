from rest_framework import serializers

from .models import Friend, Category


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['name', 'category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'order']
