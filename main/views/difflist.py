from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Medal, Music
from main.services import get_folder_status


def difflist(request: HttpRequest, sran_level: int) -> HttpResponse:
    """ 難易度表 """

    max_s_lv = 19
    sran_level = int(sran_level)

    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    music_query = Music.objects.filter(sran_level=sran_level).order_by('level', 'title')
    music_count = music_query.count()

    folder_status = Medal.ClearStatus.NO_PLAY
    if request.user.is_authenticated:
        folder_status = get_folder_status(request.user, music_query)

    paginator = Paginator(music_query, 25)
    page = request.GET.get('page')
    music_list = paginator.get_page(page)

    context = {
        'sran_level': sran_level,
        'music_list': music_list,
        'music_count': music_count,
        'folder_status': folder_status.value,
    }

    return render(request, 'main/difflist.html', context)
