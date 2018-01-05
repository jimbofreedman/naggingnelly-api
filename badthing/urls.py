from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bad_thing_types', views.BadThingTypeViewSet, base_name='bad_thing_types')
router.register(r'bad_things', views.BadThingViewSet, base_name='bad_things')

app_name = "badthing"
urlpatterns = [url(r'^', include(router.urls))]
g
