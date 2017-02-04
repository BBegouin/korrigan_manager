from django.conf.urls import include, url
from django.contrib import admin
from korrigan_manager.views import ronde1,export_ronde

from django.contrib import admin
from tournament.admin import MyAdminSite


urlpatterns = [
    url(r'^', include('tournament.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/ronde_1',ronde1,name='admin_ronde1'),
]
