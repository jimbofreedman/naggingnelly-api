from rest_framework import serializers

from .models import Action, Context, Folder, GtdUser


class GtdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GtdUser
        fields = ['bin', 'collectbox', 'actions', 'waiting_for', 'tickler', 'someday', 'updated_at']


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'updated_at']


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['id', 'name', 'glyph', 'updated_at']


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'short_description', 'status', 'priority', 'start_at', 'due_at', 'recurrence', 'dependencies',
                  'depends_on', 'folder', 'context', 'updated_at']
        read_only_fields = ['depends_on']
