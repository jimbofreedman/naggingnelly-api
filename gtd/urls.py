from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'gtd_users', views.GtdUserViewSet, base_name='gtd_users')
router.register(r'folders', views.FolderViewSet, base_name='folders')
router.register(r'contexts', views.ContextViewSet, base_name='contexts')
router.register(r'actions', views.ActionViewSet, base_name='actions')

app_name = "gtd"
urlpatterns = [url(r'^', include(router.urls))]
