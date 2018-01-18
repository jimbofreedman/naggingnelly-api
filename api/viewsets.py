from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwner


class APIViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
