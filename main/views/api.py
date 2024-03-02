from zoneinfo import ZoneInfo

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Avg, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from main.models import Bad_Count, Extra_Option, Medal, Music

from users.models import CustomUser


@require_GET
def get_clear_status(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲のクリア状況を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user and (not user.is_active or user.cleardata_privacy == 2):
        raise PermissionDenied

    bad_count = Bad_Count.objects.filter(music_id=music_id, user_id=user_id).first()
    medal_obj = Medal.objects.filter(music_id=music_id, user_id=user_id).first()
    medal = medal_obj.medal if medal_obj else None
    extra_option_exists = Extra_Option.objects.filter(music_id=music_id, user_id=user_id, hard=True).exists()

    clear_status = 'no-play'
    if medal is not None:
        if medal == 1 and bad_count == 0:
            clear_status = 'perfect'
        elif medal in [2, 3, 4] and bad_count == 0:
            clear_status = 'fullcombo'
        elif 1 <= medal <= 7 and extra_option_exists:
            clear_status = 'hard-cleared'
        elif medal in [5, 6, 7]:
            clear_status = 'cleared'
        elif medal in [8, 9, 10]:
            clear_status = 'failed'
        elif medal == 11:
            clear_status = 'easy-cleared'

    return JsonResponse({'clear_status': clear_status})


@require_GET
def get_bad_count(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲のBAD数を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user:
        if not user.is_active or user.cleardata_privacy == 2:
            raise PermissionDenied

    try:
        bad_count = Bad_Count.objects.get(music_id=music_id, user_id=user_id).bad_count
    except ObjectDoesNotExist:
        bad_count = None

    return JsonResponse({'bad_count': bad_count})


@require_GET
def get_medal(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲のメダルを返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user:
        if not user.is_active or user.cleardata_privacy == 2:
            raise PermissionDenied

    try:
        medal = Medal.objects.get(music_id=music_id, user_id=user_id).medal
    except ObjectDoesNotExist:
        medal = None

    return JsonResponse({'medal': medal})


@require_GET
def get_latest_updated_at(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲の最新の更新日時を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user:
        if not user.is_active or user.cleardata_privacy == 2:
            raise PermissionDenied

    try:
        medal = Medal.objects.get(music_id=music_id, user_id=user_id)
        updated_at = medal.updated_at.astimezone(ZoneInfo('Asia/Tokyo'))

        context = {
            'is_active': True,
            'year': updated_at.year,
            'month': updated_at.month,
            'day': updated_at.day,
            'hour': updated_at.hour,
            'minute': updated_at.minute,
            'second': updated_at.second
        }
    except ObjectDoesNotExist:
        context = {'is_active': False}

    return JsonResponse(context)


@require_GET
def get_bad_count_avg(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲の平均BAD数を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    # BAD数の平均を計算 (小数点以下四捨五入)
    bad_count_avg = Bad_Count.objects.filter(music_id=music_id).aggregate(Avg('bad_count'))['bad_count__avg']

    if bad_count_avg is None:
        bad_count_avg = -1
    else:
        bad_count_avg = round(bad_count_avg)

    return JsonResponse({'bad_count_avg': bad_count_avg})


@login_required
@require_GET
def get_myrank(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲の順位を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user:
        if not user.is_active or user.cleardata_privacy == 2:
            raise PermissionDenied

    bad_count_list = Bad_Count.objects.filter(music=music_id).order_by('bad_count')
    bad_count_num = 0
    myrank = 0
    tmp_rank = 0
    previous_bad_count = -1

    for bad_count in bad_count_list:
        # BAD数が前後で重複しない場合、順位を更新
        if bad_count.bad_count != previous_bad_count:
            tmp_rank = bad_count_num + 1

        # 自分の記録が見つかれば、myrank にランクを格納
        if bad_count.user.id == user.id:
            myrank = tmp_rank

        previous_bad_count = bad_count.bad_count
        bad_count_num += 1

    return JsonResponse({
        'myrank': myrank,
        'bad_count_num': bad_count_num
    })


@require_GET
def get_medal_count(request: HttpRequest, music_id: int) -> JsonResponse:
    """
    指定された曲の各メダルの枚数を返す
    """
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    medals = Medal.objects.filter(music_id=music_id).values('medal').annotate(total=Count('medal')).order_by('medal')

    medal_count_list = [0] * 11
    medal_count_total = 0
    for medal in medals:
        if 1 <= medal['medal'] <= 11:
            i = medal['medal'] - 1
            medal_count_list[i] = medal['total']
            medal_count_total += medal['total']

    context = {
        'medal_count_list': medal_count_list,
        'medal_count_total': medal_count_total
    }

    return JsonResponse(context)


@require_GET
def get_folder_lamp(request: HttpRequest, level: int) -> JsonResponse:
    if not is_xml_http_request(request):
        return JsonResponse({'error': 'invalid access'})

    user_id = request.GET.get('user_id', request.user.id)
    user = get_object_or_404(CustomUser, pk=user_id)

    if user != request.user and (not user.is_active or user.cleardata_privacy == 2):
        raise PermissionDenied

    is_srandom = request.GET.get('is_srandom', 'false') == 'true'
    level = int(level)
    music_query = Music.objects.filter(sran_level=level) if is_srandom else Music.objects.filter(level=50 - level + 1)

    medals = Medal.objects.filter(music__in=music_query, user=user)
    extra_options = Extra_Option.objects.filter(music__in=music_query, user=user, hard=True).values_list('music_id',
                                                                                                         flat=True)

    medal_max = 0
    easy_flg = False
    hard_flg = True if medals.exists() else False

    for music in music_query:
        medal = next((m for m in medals if m.music_id == music.id), None)
        if not medal or medal.medal == 12:
            return JsonResponse({'folder_lamp': 'no-play'})
        if medal.medal == 11:
            easy_flg = True
        if 5 <= medal.medal <= 7 and music.id not in extra_options:
            hard_flg = False
        medal_max = max(medal_max, medal.medal if medal else 0)

    if easy_flg and medal_max < 8:
        folder_lamp = 'easy-cleared'
    elif easy_flg:
        folder_lamp = 'failed'
    elif medal_max == 1:
        folder_lamp = 'perfect'
    elif 2 <= medal_max <= 4:
        folder_lamp = 'fullcombo'
    elif 5 <= medal_max <= 7:
        folder_lamp = 'hard-cleared' if hard_flg else 'cleared'
    elif 8 <= medal_max <= 10:
        folder_lamp = 'failed'
    else:
        folder_lamp = 'no-play'

    return JsonResponse({'folder_lamp': folder_lamp})


def is_xml_http_request(req: HttpRequest) -> bool:
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
