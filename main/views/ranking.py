from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, OuterRef, Prefetch, Subquery
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Bad_Count, Extra_Option, Medal, Music, Sran_Level
from main.services import get_folder_status


@login_required
def ranking(request: HttpRequest, sran_level: int) -> HttpResponse:
    """ ランキング """

    if sran_level <= 0 or sran_level > Sran_Level.MAX:
        raise Http404

    music_query = Music.objects.filter(sran_level=sran_level).order_by('level', 'title').select_related(
        'difficulty', 'level')
    music_count = music_query.count()

    folder_status = get_folder_status(request.user, music_query)

    bad_count_avg_subquery = Bad_Count.objects.filter(music=OuterRef('pk')).order_by().values('music').annotate(
        avg=Avg('bad_count')).values('avg')

    music_query = music_query.prefetch_related(
        Prefetch('bad_count_set', queryset=Bad_Count.objects.filter(user=request.user), to_attr='user_bad_count'),
        Prefetch('medal_set', queryset=Medal.objects.filter(user=request.user), to_attr='user_medal'),
        Prefetch('extra_option_set', queryset=Extra_Option.objects.filter(user=request.user, hard=True),
                 to_attr='user_extra_option')
    ).annotate(
        bad_count_avg=Subquery(bad_count_avg_subquery),
    )

    music_data = []
    for music in music_query:
        bad_count = None
        medal = None
        extra_option = None
        clear_status = Medal.ClearStatus.NO_PLAY.value

        bad_count_avg = round(music.bad_count_avg) if music.bad_count_avg is not None else None

        if hasattr(music, 'user_medal') and music.user_medal:
            medal = music.user_medal[0]

        if hasattr(music, 'user_extra_option') and music.user_extra_option:
            extra_option = music.user_extra_option[0]

        if hasattr(music, 'user_bad_count') and music.user_bad_count:
            bad_count = music.user_bad_count[0]

        if medal:
            clear_status = medal.get_clear_status(bad_count=bad_count, extra_option=extra_option).value

        music_data.append({
            'id': music.id,
            'level': music.level.level,
            'title': music.title,
            'difficulty': music.difficulty.difficulty_short(),
            'bad_count': bad_count.int() if bad_count else None,
            'bad_count_avg': bad_count_avg,
            'clear_status': clear_status,
        })

    paginator = Paginator(music_data, 25)
    page = request.GET.get('page')
    music_list = paginator.get_page(page)

    context = {
        'sran_level': sran_level,
        'music_list': music_list,
        'music_count': music_count,
        'folder_status': folder_status.value,
    }

    return render(request, 'main/ranking.html', context)
