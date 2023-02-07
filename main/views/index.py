from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.forms import SearchForm
from main.models import Medal, Music
from social_django.models import UserSocialAuth


def index(request: HttpRequest) -> HttpResponse:
    """ トップページ """

    medal_num = Medal.objects.all().count()
    recent_medal = Medal.objects.all().order_by('-updated_at')[:10]
    recent_music_id_list = list(recent_medal.values_list('music', flat=True))
    recent_music = []
    for recent_music_id in recent_music_id_list:
        recent_music.append(Music.objects.get(pk=recent_music_id))
    search_form = SearchForm(request.GET)

    is_signed_in_with_google = False
    user = request.user
    if user.is_authenticated:
        socials = UserSocialAuth.objects.filter(user=user, provider="google-oauth2")
        if len(socials) != 0:
            is_signed_in_with_google = True

    context = {
        'medal_num': medal_num,
        'recent_music': recent_music,
        'search_form': search_form,
        'is_signed_in_with_google': is_signed_in_with_google
    }
    return render(request, 'main/index.html', context)
