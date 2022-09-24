from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('settings/', views.settings, name='settings'),
    path('deactivate/', views.deactivate, name='deactivate'),
    path('<username>/', views.mypage, name='mypage'),
    path('<username>/statistics/', views.statistics, name='statistics'),
    path('<username>/cleardata/<int:sran_level>/',
         views.cleardata, name='cleardata'),
    path('download/<file_type>/', views.download, name='download'),
    path('api/get_percentage_of_clear/<int:user_id>/',
         views.get_percentage_of_clear, name='get_percentage_of_clear'),
    path('api/get_activity_map/', views.get_activity_map, name='get_activity_map'),
    path('api/get_clear_rate/', views.get_clear_rate, name='get_clear_rate'),
]
