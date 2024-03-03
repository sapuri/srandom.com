from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Bad_Count, Extra_Option, Medal, Music


def ranking_detail(request: HttpRequest, music_id: int) -> HttpResponse:
    music = get_object_or_404(Music, pk=music_id)

    medals = Medal.objects.filter(music=music).select_related('user')
    extra_options = Extra_Option.objects.filter(music=music, hard=True).select_related('user')

    medals_dict = {medal.user.id: medal for medal in medals}
    extra_options_dict = {option.user.id: option for option in extra_options}

    bad_count_list = Bad_Count.objects.filter(music=music).order_by('bad_count', 'updated_at')
    bad_count_avg_result = bad_count_list.aggregate(Avg('bad_count'))
    bad_count_avg = round(bad_count_avg_result['bad_count__avg']) if bad_count_avg_result[
        'bad_count__avg'] is not None else None

    rank, last_bad_count, results = 1, None, []

    for i, bad_count in enumerate(bad_count_list, start=1):
        if bad_count.bad_count != last_bad_count:
            rank = i
        last_bad_count = bad_count.bad_count

        medal = medals_dict.get(bad_count.user.id)
        extra_option = extra_options_dict.get(bad_count.user.id)

        if medal is None:
            status = Medal.ClearStatus.NO_PLAY.value
        else:
            status = medal.get_clear_status(bad_count, extra_option).value

        results.append({
            'rank': rank,
            'user': bad_count.user,
            'medal': medal,
            'bad_count': bad_count,
            'extra_option': extra_option,
            'status': status,
        })

    context = {
        'music': music,
        'bad_count_avg': bad_count_avg,
        'results': results,
    }

    return render(request, 'main/ranking_detail.html', context)
