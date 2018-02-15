from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name='news'),
    path('search/', views.search, name='search'),
    path('level/', views.level_select, name='level_select'),
    path('level/<int:level>/', views.level, name='level'),
    path('difflist/', views.difflist_level_select, name='difflist_level_select'),
    path('difflist/<int:sran_level>/', views.difflist, name='difflist'),
    path('edit/<int:music_id>/', views.edit, name='edit'),
    path('ranking/', views.ranking_level_select, name='ranking_level_select'),
    path('ranking/<int:sran_level>/', views.ranking, name='ranking'),
    path('ranking/detail/<int:music_id>/', views.ranking_detail, name='ranking_detail'),
    path('omikuji/', views.omikuji, name='omikuji'),
    path('premium/', views.premium, name='premium'),
    path('api/get_clear_status/<int:music_id>/', views.get_clear_status, name='get_clear_status'),
    path('api/get_bad_count/<int:music_id>/', views.get_bad_count, name='get_bad_count'),
    path('api/get_medal/<int:music_id>/', views.get_medal, name='get_medal'),
    path('api/get_latest_updated_at/<int:music_id>/', views.get_latest_updated_at, name='get_latest_updated_at'),
    path('api/get_bad_count_avg/<int:music_id>/', views.get_bad_count_avg, name='get_bad_count_avg'),
    path('api/get_myrank/<int:music_id>/', views.get_myrank, name='get_myrank'),
    path('api/get_medal_count/<int:music_id>/', views.get_medal_count, name='get_medal_count'),
    path('api/get_folder_lamp/<int:level>/', views.get_folder_lamp, name='get_folder_lamp'),
]
