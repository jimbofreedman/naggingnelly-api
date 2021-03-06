from django.db.models import Max
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.viewsets import APIViewSet

from .models import Action
from .serializers import ActionSerializer, ContextSerializer, FolderSerializer, GtdUserSerializer

response = HttpResponseRedirect('/dashboard')


class PollViewSet(viewsets.ModelViewSet):
    def list(self, request):
        return Response({
            "actions": request.user.action_set.aggregate(Max('updated_at'))['updated_at__max'],
            "contexts": request.user.context_set.aggregate(Max('updated_at'))['updated_at__max'],
            "folders": request.user.folder_set.aggregate(Max('updated_at'))['updated_at__max']
        })


class GtdUserViewSet(viewsets.ModelViewSet):
    serializer_class = GtdUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [self.request.user.gtd_user]  # ew that's horrible
        else:
            return None


class FolderViewSet(APIViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self):
        return self.request.user.folder_set.all()


class ContextViewSet(APIViewSet):
    serializer_class = ContextSerializer

    def get_queryset(self):
        return self.request.user.context_set.all()


class ActionViewSet(APIViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        return self.request.user.action_set.prefetch_related("dependencies", "depends_on")

    @detail_route(methods=['post'])
    def complete(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        action.status = Action.STATUS_COMPLETED
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def cancel(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        action.status = Action.STATUS_CANCELLED
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def fail(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        action.status = Action.STATUS_FAILED
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def add_dependency(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        dependency = Action.objects.get(owner=request.user, pk=request.GET.get('dependency_action_id', None))
        action.dependencies.add(dependency)
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def remove_dependency(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        dependency = Action.objects.get(owner=request.user, pk=request.GET.get('dependency_action_id', None))
        action.dependencies.remove(dependency)
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def reprioritise_after(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        after_action_priority = Action.objects.get(owner=request.user, pk=request.data['after_action_id']).priority
        before_action_priority = Action.objects.get(owner=request.user, priority__lt=after_action_priority,
                                                    status=Action.STATUS_OPEN).priority

        action.priority = int((before_action_priority + after_action_priority) / 2)
        action.save()
        return Response(self.get_serializer(action).data)
