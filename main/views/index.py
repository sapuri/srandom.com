from django.shortcuts import render

from main.forms import SearchForm
from main.models import Medal, Music


def index(request):
    """ トップページ """
    medal_num = Medal.objects.all().count()
    recent_medal = Medal.objects.all().order_by('-updated_at')[:10]
    recent_music_id_list = list(recent_medal.values_list('music', flat=True))
    recent_music = []
    for recent_music_id in recent_music_id_list:
        recent_music.append(Music.objects.get(pk=recent_music_id))
    search_form = SearchForm(request.GET)

    context = {
        'medal_num': medal_num,
        'recent_music': recent_music,
        'search_form': search_form
    }
    return render(request, 'main/index.html', context)
