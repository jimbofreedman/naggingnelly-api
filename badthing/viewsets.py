from .serializers import BadThingSerializer, BadThingTypeSerializer
from api.viewsets import APIViewSet

class BadThingTypeViewSet(APIViewSet):
    serializer_class = BadThingTypeSerializer

    def get_queryset(self):
        return self.request.user.badthingtype_set.all()


class BadThingViewSet(APIViewSet):
    serializer_class = BadThingSerializer

    def get_queryset(self):
        return self.request.user.badthing_set.all()
