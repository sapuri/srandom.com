from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Music


def level(request: HttpRequest, level: int) -> HttpResponse:
    """ 難易度表 """

    # 最大レベル
    max_lv = 50

    # レベルが不正なら404エラー
    if level <= 0 or level > max_lv:
        raise Http404

    # レベルIDを求める
    level_id = max_lv - level + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(level=level_id).order_by('-sran_level', 'title')

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

    context = {
        'level': level,
        'music_list': music_list,
        'music_list_count': len(music_list)
    }

    return render(request, 'main/level/level.html', context)
