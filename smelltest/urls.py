from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /smelltest/
    url(r'^$', views.index, name='index'),
    url(r'^data$', views.data, name='data'),
]
