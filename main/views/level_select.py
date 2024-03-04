from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Level


def level_select(request: HttpRequest) -> HttpResponse:
    """ 公式難易度表: レベル選択 """

    lv_range = range(Level.MAX, Level.MIN - 1, -1)

    context = {
        'lv_range': lv_range
    }

    return render(request, 'main/level/level_select.html', context)
