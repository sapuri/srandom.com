from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from main.models import Medal, Sran_Level

from users.models import CustomUser


def mypage(request: HttpRequest, username: str):
    """ マイページ (プロフィールページ) """

    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    s_lv_range = range(Sran_Level.MAX, Sran_Level.MIN - 1, -1)

    recent_medal = Medal.objects.filter(user=selected_user).order_by('-updated_at')[:20]

    context = {
        'selected_user': selected_user,
        's_lv_range': s_lv_range,
        'recent_medal': recent_medal
    }
    return render(request, 'users/mypage.html', context)
