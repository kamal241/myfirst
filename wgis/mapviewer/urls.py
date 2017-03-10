from mapviewer import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^weather$', views.weather, name='weather_vector'),
    url(r'^weather_swave$', views.weather_swave, name='weather_swave'),
    url(r'^weather_raster$', views.weather_raster, name='weather_raster'),
    url(r'^reports/location$', views.reports_location, name='reports')
]
