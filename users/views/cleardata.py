from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Music, Medal, Bad_Count, Extra_Option
from users.models import CustomUser


def cleardata(request: HttpRequest, username: str, sran_level: int) -> HttpResponse:
    """ クリア状況 """

    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    # 最大S乱レベル
    max_s_lv = 19

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    # S乱レベルID
    sran_level_id = sran_level

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

    # ページング
    paginator = Paginator(music_list, 25)
    page = request.GET.get('page')

    try:
        music_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        music_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        music_list = paginator.page(paginator.num_pages)

    # ユーザーごとにデータを取得
    medal_list = Medal.objects.filter(user=selected_user)
    bad_count_list = Bad_Count.objects.filter(user=selected_user)
    extra_option_list = Extra_Option.objects.filter(user=selected_user)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': len(music_list),
        'medal_list': medal_list,
        'bad_count_list': bad_count_list,
        'extra_option_list': extra_option_list
    }
    return render(request, 'users/cleardata.html', context)
