from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from main.models import Bad_Count, Extra_Option, Medal, Sran_Level

from users.models import CustomUser


def mypage(request: HttpRequest, username: str):
    """ マイページ (プロフィールページ) """

    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    s_lv_range = range(Sran_Level.MAX, Sran_Level.MIN - 1, -1)

    recent_medal = Medal.objects.filter(user=selected_user).order_by('-updated_at').select_related('music',
                                                                                                   'music__level',
                                                                                                   'music__sran_level',
                                                                                                   'music__difficulty')[
        :20]

    recent_data = []
    for medal in recent_medal:
        music = medal.music
        bad_count = Bad_Count.objects.filter(user=selected_user, music=music).first()
        extra_option = Extra_Option.objects.filter(user=selected_user, music=music, hard=True).first()

        clear_status = medal.get_clear_status(bad_count=bad_count, extra_option=extra_option).value

        recent_data.append({
            'music_id': music.id,
            'level': music.level.level,
            'sran_level': music.sran_level.level,
            'title': music.title,
            'difficulty': music.difficulty.difficulty_short(),
            'bpm': music.bpm,
            'medal': medal.medal,
            'bad_count': bad_count.bad_count if bad_count else None,
            'updated_at': medal.updated_at,
            'clear_status': clear_status,
        })

    context = {
        'selected_user': selected_user,
        's_lv_range': s_lv_range,
        'recent_data': recent_data
    }
    return render(request, 'users/mypage.html', context)
