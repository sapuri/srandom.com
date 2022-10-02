from django.shortcuts import get_object_or_404, render

from main.models import Medal
from users.models import CustomUser


def mypage(request, username):
    """
    マイページ (プロフィールページ)
    @param username: ユーザー名
    """
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    max_s_lv = 19
    s_lv_range = range(max_s_lv, 0, -1)

    recent_medal = Medal.objects.filter(user=selected_user).order_by('-updated_at')[:20]

    context = {
        'selected_user': selected_user,
        's_lv_range': s_lv_range,
        'recent_medal': recent_medal
    }
    return render(request, 'users/mypage.html', context)
