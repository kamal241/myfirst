from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'wgis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mapviewer/', include('mapviewer.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
