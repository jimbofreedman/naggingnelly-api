from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views, viewsets

router = DefaultRouter()
router.register(r'friends', viewsets.FriendViewSet, base_name='friends')
router.register(r'categories', viewsets.CategoryViewSet, base_name='categories')

app_name = "friendtracker"
urlpatterns = [
    url(r'^update', views.UpdateListView.as_view()),
    url(r'^list', views.list),
    url(r'^categorize(/(?P<friend_id>\d+)/(?P<category_id>\d+)/)?$', views.categorize),
    url(r'^', include(router.urls)),
]
