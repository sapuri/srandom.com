from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Level, Medal, Music
from main.services import get_folder_status


def level(request: HttpRequest, level: int) -> HttpResponse:
    """ 難易度表 """

    if level <= 0 or level > Level.MAX:
        raise Http404

    level_id = Level.MAX - level + 1

    music_query = Music.objects.filter(level=level_id).order_by('-sran_level', 'title')
    music_count = music_query.count()

    folder_status = Medal.ClearStatus.NO_PLAY
    if request.user.is_authenticated:
        folder_status = get_folder_status(request.user, music_query)

    paginator = Paginator(music_query, 25)
    page = request.GET.get('page')
    music_list = paginator.get_page(page)

    context = {
        'level': level,
        'music_list': music_list,
        'music_count': music_count,
        'folder_status': folder_status.value,
    }

    return render(request, 'main/level/level.html', context)
