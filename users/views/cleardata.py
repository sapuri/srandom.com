from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Bad_Count, Extra_Option, Medal, Music, Sran_Level

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

    # ユーザーごとにデータを取得
    medal_list = Medal.objects.filter(user=selected_user)
    bad_count_list = Bad_Count.objects.filter(user=selected_user)
    extra_option_list = Extra_Option.objects.filter(user=selected_user)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': music_count,
        'medal_list': medal_list,
        'bad_count_list': bad_count_list,
        'extra_option_list': extra_option_list
    }
    return render(request, 'users/cleardata.html', context)
