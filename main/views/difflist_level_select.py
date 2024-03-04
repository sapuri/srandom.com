from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Sran_Level


def difflist_level_select(request: HttpRequest) -> HttpResponse:
    """ 難易度表: S乱レベル選択 """

    s_lv_range = range(Sran_Level.MAX, Sran_Level.MIN - 1, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/difflist_level_select.html', context)
