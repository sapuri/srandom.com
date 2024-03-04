from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Music, Sran_Level
from main.services import get_folder_status

from users.models import CustomUser


def cleardata(request: HttpRequest, username: str, sran_level: int) -> HttpResponse:
    """ クリア状況 """

    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    if sran_level <= 0 or sran_level > Sran_Level.MAX:
        raise Http404

    music_query = Music.objects.filter(sran_level=sran_level).order_by('level', 'title')
    music_count = music_query.count()

    paginator = Paginator(music_query, 25)
    page = request.GET.get('page')
    music_list = paginator.get_page(page)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
        'music_count': music_count,
        'folder_status': get_folder_status(selected_user, music_query).value,
    }
    return render(request, 'users/cleardata.html', context)
