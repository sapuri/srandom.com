from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def level_select(request: HttpRequest) -> HttpResponse:
    """ 公式難易度表: レベル選択 """

    max_lv = 50

    min_lv = 38

    lv_range = range(max_lv, min_lv - 1, -1)

    context = {
        'lv_range': lv_range
    }

    return render(request, 'main/level/level_select.html', context)
