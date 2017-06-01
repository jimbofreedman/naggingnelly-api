from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .serializers import ActionSerializer
from .models import Action

response = HttpResponseRedirect('/dashboard')


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.action_set.all()
        else:
            return None

    @detail_route(methods=['post'])
    def complete(self, request, pk=None):
        action = Action.objects.get(owner=request.user,pk=pk)
        action.status = Action.STATUS_COMPLETED
        action.save()
        return Response(self.get_serializer(action).data)
