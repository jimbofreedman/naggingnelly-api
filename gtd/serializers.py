from rest_framework import serializers
from .models import GtdUser, Folder, Context, Action


class GtdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GtdUser
        fields = ['bin', 'collectbox', 'actions', 'waiting_for', 'tickler', 'someday']


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name']


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['id', 'name', 'glyph']


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'short_description', 'status', 'priority', 'start_at', 'due_at', 'recurrence', 'dependencies',
                  'folder', 'context']
