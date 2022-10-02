from django.urls import path

from .views import api, cleardata, deactivate, download, list, mypage, settings, statistics

app_name = 'users'
urlpatterns = [
    path('list/', list.list_users, name='list'),
    path('settings/', settings.settings, name='settings'),
    path('deactivate/', deactivate.deactivate, name='deactivate'),
    path('<username>/', mypage.mypage, name='mypage'),
    path('<username>/statistics/', statistics.statistics, name='statistics'),
    path('<username>/cleardata/<int:sran_level>/', cleardata.cleardata, name='cleardata'),
    path('download/<file_type>/', download.download, name='download'),
    path('api/get_percentage_of_clear/<int:user_id>/', api.get_percentage_of_clear, name='get_percentage_of_clear'),
    path('api/get_activity_map/', api.get_activity_map, name='get_activity_map'),
    path('api/get_clear_rate/', api.get_clear_rate, name='get_clear_rate'),
]
