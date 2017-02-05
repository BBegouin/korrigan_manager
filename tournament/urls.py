from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^match/(?P<match_id>[0-9]+)/$', views.match, name='match'),
    url(r'^export/xls/ronde/(?P<ronde_id>[0-9]+)/$', views.export_xls_ronde, name='export_xls_ronde'),
    url(r'^export/xls/ranking/$', views.export_xls_ranking, name='export_xls_ranking'),
    url(r'^admin/ronde/(?P<ronde_id>[0-9]+)/$', views.admin_view_ronde, name='admin_view_ronde'),
    url(r'^admin/ronde/draw/(?P<ronde_id>[0-9]+)/(?P<cancel_ronde_id>[0-9]+)$', views.draw_ronde, name='admin_draw_ronde'),
]