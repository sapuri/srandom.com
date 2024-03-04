from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def difflist_level_select(request: HttpRequest) -> HttpResponse:
    """ 難易度表: S乱レベル選択 """

    max_s_lv = 19

    s_lv_range = range(max_s_lv, 0, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/difflist_level_select.html', context)
