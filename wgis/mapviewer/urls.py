from mapviewer import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^weather$', views.weather, name='weather')
]