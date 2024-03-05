from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.forms import SearchForm
from main.models import Medal, Music

from social_django.models import UserSocialAuth


def index(request: HttpRequest) -> HttpResponse:
    """ トップページ """

    medal_num = Medal.objects.count()
    recent_medals = Medal.objects.order_by('-updated_at')[:10]

    recent_music_ids = list(recent_medals.values_list('music', flat=True))
    recent_music = Music.objects.filter(id__in=recent_music_ids)

    search_form = SearchForm(request.GET)

    user_google_ids = []
    if request.user.is_authenticated:
        user_google_ids = UserSocialAuth.objects.filter(user=request.user, provider="google-oauth2").values_list('uid',
                                                                                                                 flat=True)

    context = {
        'medal_num': medal_num,
        'recent_music': recent_music,
        'search_form': search_form,
        'is_signed_in_with_google': bool(user_google_ids),
        'user_google_ids': user_google_ids,
    }
    return render(request, 'main/index.html', context)
