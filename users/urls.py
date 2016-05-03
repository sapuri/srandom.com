from django.conf.urls import include, url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^list/$', views.list, name='list'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^deactivate/$', views.deactivate, name='deactivate'),
    url(r'^(?P<username>\w+)/$', views.mypage, name='mypage'),
    url(r'^(?P<username>\w+)/cleardata/(?P<sran_level>\d+)/$', views.cleardata, name='cleardata'),
]
