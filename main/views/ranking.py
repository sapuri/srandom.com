from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render

from main.models import Music


@login_required
def ranking(request, sran_level):
    """
    ランキング
    @param sran_level: S乱レベル
    """
    # 最高S乱レベル
    max_s_lv = 19

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    sran_level_id = sran_level

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

    # 取得曲数を取得
    music_list_count = len(music_list)

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
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': music_list_count
    }

    return render(request, 'main/ranking.html', context)
