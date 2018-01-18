from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets

from .serializers import BadThingSerializer, BadThingTypeSerializer

response = HttpResponseRedirect('/dashboard')


class BadThingTypeViewSet(viewsets.ModelViewSet):
    serializer_class = BadThingTypeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.badthingtype_set.all()
        else:
            return None


class BadThingViewSet(viewsets.ModelViewSet):
    serializer_class = BadThingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.request.user.badthing_set.all()
        else:
            return None
