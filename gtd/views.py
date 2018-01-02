from graphviz import Digraph
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .serializers import GtdUserSerializer, FolderSerializer, ContextSerializer, ActionSerializer
from .models import Action

response = HttpResponseRedirect('/dashboard')


class GtdUserViewSet(viewsets.ModelViewSet):
    serializer_class = GtdUserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [self.request.user.gtd_user]  # ew that's horrible
        else:
            return None


class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.folder_set.all()
        else:
            return None


class ContextViewSet(viewsets.ModelViewSet):
    serializer_class = ContextSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.context_set.all()
        else:
            return None


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.folder = instance.owner.gtd_user.bin
        instance.save()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.action_set.all()
        else:
            return None

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
        dependency = Action.objects.get(owner=request.user, pk=request.data['dependency_action_id'])
        action.dependencies.add(dependency)
        action.save()
        return Response(self.get_serializer(action).data)

    @detail_route(methods=['post'])
    def remove_dependency(self, request, pk=None):
        action = Action.objects.get(owner=request.user, pk=pk)
        dependency = Action.objects.get(owner=request.user, pk=request.data['dependency_action_id'])
        action.dependencies.remove(dependency)
        action.save()
        return Response(self.get_serializer(action).data)

    def _get_graph(self, format):
        dot = Digraph(format=format, comment='Tasks', graph_attr={"rankdir": "LR"})
        actions = self.get_queryset().filter(status=Action.STATUS_OPEN)
        for a in actions:
            dot.node(str(a.id), a.short_description)
            for d in a.depends_on.all():
                dot.edge(str(a.id), str(d.id))
        return dot

    @list_route(methods=['get'])
    def graph_png(self, request):
        return HttpResponse(self._get_graph("png").pipe(), content_type="image/png")

    @list_route(methods=['get'])
    def graph_json(self, request):
        return HttpResponse(self._get_graph("json").pipe(), content_type="application/json")

    @list_route(methods=['get'])
    def graph_svg(self, request):
        return HttpResponse(self._get_graph("svg").pipe(), content_type="text/plain")
