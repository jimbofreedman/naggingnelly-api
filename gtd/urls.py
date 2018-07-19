from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(r'poll', viewsets.PollViewSet, base_name='poll')
router.register(r'gtd_users', viewsets.GtdUserViewSet, base_name='gtd_users')
router.register(r'folders', viewsets.FolderViewSet, base_name='folders')
router.register(r'contexts', viewsets.ContextViewSet, base_name='contexts')
router.register(r'actions', viewsets.ActionViewSet, base_name='actions')

app_name = "gtd"
urlpatterns = [url(r'^', include(router.urls))]
