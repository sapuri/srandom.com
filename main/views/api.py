from zoneinfo import ZoneInfo

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Avg, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from main.models import Bad_Count, Extra_Option, Medal, Music
from main.services import get_folder_status

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
    medal = Medal.objects.filter(music_id=music_id, user_id=user_id).first()
    extra_option = Extra_Option.objects.filter(music_id=music_id, user_id=user_id, hard=True).first()

    clear_status = Medal.ClearStatus.NO_PLAY.value
    if medal:
        clear_status = medal.get_clear_status(bad_count=bad_count, extra_option=extra_option).value

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

    folder_status = get_folder_status(user, music_query)

    return JsonResponse({'folder_lamp': folder_status.value})


def is_xml_http_request(req: HttpRequest) -> bool:
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
