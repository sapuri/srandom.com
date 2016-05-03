from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^level/$', views.level_select, name='level_select'),
    url(r'^level/(?P<level>\d+)/$', views.level, name='level'),
    url(r'^difflist/$', views.difflist_level_select, name='difflist_level_select'),
    url(r'^difflist/all/$', views.difflist_all, name='difflist_all'),
    url(r'^difflist/(?P<sran_level>\d+)/$', views.difflist, name='difflist'),
    url(r'^edit/(?P<music_id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<music_id>\d+)/$', views.delete, name='delete'),
    url(r'^ranking/$', views.ranking_level_select, name='ranking_level_select'),
    url(r'^ranking/(?P<sran_level>\d+)/$', views.ranking, name='ranking'),
    url(r'^ranking/detail/(?P<music_id>\d+)/$', views.ranking_detail, name='ranking_detail'),
    url(r'^omikuji/$', views.omikuji, name='omikuji'),
    url(r'^premium/$', views.premium, name='premium'),
]
