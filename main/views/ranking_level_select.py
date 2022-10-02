from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def ranking_level_select(request):
    """
    ランキング: S乱レベル選択
    """
    # 最大S乱レベル
    max_s_lv = 19

    s_lv_range = range(max_s_lv, 0, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/ranking_level_select.html', context)
