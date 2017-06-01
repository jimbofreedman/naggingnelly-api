from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'actions', views.ActionViewSet, base_name='actions')

app_name = "gtd"
urlpatterns = [url(r'^', include(router.urls))]
