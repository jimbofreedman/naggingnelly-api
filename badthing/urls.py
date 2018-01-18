from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(r'bad_thing_types', viewsets.BadThingTypeViewSet, base_name='bad_thing_types')
router.register(r'bad_things', viewsets.BadThingViewSet, base_name='bad_things')

app_name = "badthing"
urlpatterns = [url(r'^', include(router.urls))]
