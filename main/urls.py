from django.urls import path

from .views import api, difflist, difflist_level_select, edit, index, level, level_select, news, omikuji, premium, ranking, ranking_detail, ranking_level_select, search

app_name = 'main'
urlpatterns = [
    path('', index.index, name='index'),
    path('news/', news.news, name='news'),
    path('search/', search.search, name='search'),
    path('level/', level_select.level_select, name='level_select'),
    path('level/<int:level>/', level.level, name='level'),
    path('difflist/', difflist_level_select.difflist_level_select, name='difflist_level_select'),
    path('difflist/<int:sran_level>/', difflist.difflist, name='difflist'),
    path('edit/<int:music_id>/', edit.edit, name='edit'),
    path('ranking/', ranking_level_select.ranking_level_select, name='ranking_level_select'),
    path('ranking/<int:sran_level>/', ranking.ranking, name='ranking'),
    path('ranking/detail/<int:music_id>/', ranking_detail.ranking_detail, name='ranking_detail'),
    path('omikuji/', omikuji.omikuji, name='omikuji'),
    path('premium/', premium.premium, name='premium'),
    path('api/get_clear_status/<int:music_id>/', api.get_clear_status, name='get_clear_status'),
    path('api/get_bad_count/<int:music_id>/', api.get_bad_count, name='get_bad_count'),
    path('api/get_medal/<int:music_id>/', api.get_medal, name='get_medal'),
    path('api/get_latest_updated_at/<int:music_id>/', api.get_latest_updated_at, name='get_latest_updated_at'),
    path('api/get_bad_count_avg/<int:music_id>/', api.get_bad_count_avg, name='get_bad_count_avg'),
    path('api/get_myrank/<int:music_id>/', api.get_myrank, name='get_myrank'),
    path('api/get_medal_count/<int:music_id>/', api.get_medal_count, name='get_medal_count'),
    path('api/get_folder_lamp/<int:level>/', api.get_folder_lamp, name='get_folder_lamp'),
]
