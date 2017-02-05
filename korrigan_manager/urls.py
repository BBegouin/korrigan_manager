from django.conf.urls import include, url
from django.contrib import admin

from django.contrib import admin
from tournament.admin import MyAdminSite


urlpatterns = [
    url(r'^', include('tournament.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
