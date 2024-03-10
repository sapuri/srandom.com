from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Bad_Count, Extra_Option, Medal, Music, Sran_Level
from main.services import get_folder_status

from users.models import CustomUser


def cleardata(request: HttpRequest, username: str, sran_level: int) -> HttpResponse:
    """ クリア状況 """

    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    if sran_level <= 0 or sran_level > Sran_Level.MAX:
        raise Http404

    music_query = Music.objects.filter(sran_level=sran_level).order_by('level', 'title').select_related('difficulty',
                                                                                                        'level')
    music_count = music_query.count()

    music_query = music_query.prefetch_related(
        Prefetch('medal_set', queryset=Medal.objects.filter(user=selected_user), to_attr='user_medal'),
        Prefetch('bad_count_set', queryset=Bad_Count.objects.filter(user=selected_user), to_attr='user_bad_count'),
        Prefetch('extra_option_set', queryset=Extra_Option.objects.filter(user=selected_user, hard=True),
                 to_attr='user_extra_option')
    )

    music_data = []
    for music in music_query:
        medal = None
        bad_count = None
        extra_option = None
        clear_status = Medal.ClearStatus.NO_PLAY.value
        updated_at = None

        if hasattr(music, 'user_medal') and music.user_medal:
            medal = music.user_medal[0]
            updated_at = medal.updated_at

        if hasattr(music, 'user_bad_count') and music.user_bad_count:
            bad_count = music.user_bad_count[0]
            if not updated_at or bad_count.updated_at > updated_at:
                updated_at = bad_count.updated_at

        if hasattr(music, 'user_extra_option') and music.user_extra_option:
            extra_option = music.user_extra_option[0]

        if medal:
            clear_status = medal.get_clear_status(bad_count=bad_count, extra_option=extra_option).value

        music_data.append({
            'id': music.id,
            'level': music.level.level,
            'title': music.title,
            'difficulty': music.difficulty.difficulty_short(),
            'bpm': music.bpm,
            'medal': medal.medal if medal else None,
            'bad_count': bad_count.bad_count if bad_count else None,
            'clear_status': clear_status,
            'updated_at': updated_at,
        })

    paginator = Paginator(music_data, 25)
    page = request.GET.get('page')
    music_list = paginator.get_page(page)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
        'music_count': music_count,
        'folder_status': get_folder_status(selected_user, music_query).value,
    }
    return render(request, 'users/cleardata.html', context)
