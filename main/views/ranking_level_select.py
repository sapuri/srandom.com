from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Sran_Level


@login_required
def ranking_level_select(request: HttpRequest) -> HttpResponse:
    """ ランキング: S乱レベル選択 """

    s_lv_range = range(Sran_Level.MAX, Sran_Level.MIN - 1, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/ranking_level_select.html', context)
