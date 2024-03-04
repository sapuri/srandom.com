from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Activity

from users.models import CustomUser


def statistics(request: HttpRequest, username: str) -> HttpResponse:
    """ 統計情報 """

    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)
    activity_count = Activity.objects.filter(user=selected_user).count()

    context = {
        'selected_user': selected_user,
        'activity_count': activity_count
    }
    return render(request, 'users/statistics.html', context)
