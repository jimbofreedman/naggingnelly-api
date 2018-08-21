from api.viewsets import APIViewSet

from .serializers import FriendSerializer, CategorySerializer


class FriendViewSet(APIViewSet):
    serializer_class = FriendSerializer

    def get_queryset(self):
        return self.request.user.friend_set.all()


class CategoryViewSet(APIViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.request.user.category_set.all()
