import json
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpRequest
from django.shortcuts import get_object_or_404

from main.models import Music, Medal, Activity, Extra_Option
from users.models import CustomUser


def get_percentage_of_clear(request, user_id):
    """
    指定されたユーザーの各レベルのクリア率を返す
    @param {int} user_id ユーザーID
    @return {json} 各レベルのクリア率
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        user = get_object_or_404(CustomUser, pk=user_id)

        # 権限を確認
        if user != request.user:
            if not user.is_active or user.cleardata_privacy == 2:
                raise PermissionDenied

        max_s_lv = 19
        s_lv_range = range(max_s_lv, 0, -1)

        music_num = [0] * max_s_lv
        clear_num = [0] * max_s_lv
        percentage_of_clear = [0] * max_s_lv

        for sran_level in s_lv_range:
            sran_level_id = sran_level
            music_list = Music.objects.filter(sran_level=sran_level_id)
            music_num[sran_level - 1] = len(music_list)
            for music in music_list:
                try:
                    medal = Medal.objects.get(user=user, music=music)
                    if medal.medal <= 7:
                        clear_num[sran_level - 1] = clear_num[sran_level - 1] + 1
                except Exception:
                    pass

            # 各レベルのクリア率を計算
            percentage_of_clear[sran_level - 1] = clear_num[sran_level - 1] * 100 / music_num[sran_level - 1]
            # 小数点以下四捨五入
            percentage_of_clear[sran_level - 1] = round(percentage_of_clear[sran_level - 1])

        context = {
            'percentage_of_clear': percentage_of_clear,
            'music_num': music_num,
            'clear_num': clear_num
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')


def get_activity_map(request):
    # パラメータチェック
    if ('user_id' not in request.GET) or ('start' not in request.GET) or ('stop' not in request.GET):
        raise Http404()

    user_id = request.GET['user_id']
    user = get_object_or_404(CustomUser, pk=user_id)

    # 権限を確認
    if user != request.user:
        if not user.is_active or user.cleardata_privacy == 2:
            raise PermissionDenied

    start = int(request.GET['start'])
    end = int(request.GET['stop'])

    start_datetime = datetime.fromtimestamp(start / 1000.0, tz=ZoneInfo('Asia/Tokyo'))
    end_datetime = datetime.fromtimestamp(end / 1000.0, tz=ZoneInfo('Asia/Tokyo'))

    activities = Activity.objects.filter(user=user_id, updated_at__range=(start_datetime, end_datetime))
    result = {}
    for activity in activities:
        updated_at = str(int(datetime.timestamp(activity.updated_at)))
        if updated_at in result:
            result[updated_at] += 1
        else:
            result.update({updated_at: 1})

    json_str = json.dumps(result, ensure_ascii=False)
    return HttpResponse(json_str, content_type='application/json; charset=UTF-8')


def get_clear_rate(request):
    # パラメータチェック
    if 'user_id' not in request.GET:
        raise Http404()

    user_id = request.GET['user_id']
    user = get_object_or_404(CustomUser, pk=user_id)

    max_s_lv = 19
    s_lv_range = range(max_s_lv, 0, -1)

    chart_data = {
        'clearRate': {
            'labels': [],
            'datasets': [{
                'label': 'Perfect',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1
            }, {
                'label': 'Full Combo',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1
            }, {
                'label': 'Hard Clear',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1
            }, {
                'label': 'Clear',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1
            }, {
                'label': 'Easy Clear',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1
            }, {
                'label': 'Failed',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 1,
            }, {
                'label': 'No Play',
                'data': [],
                'backgroundColor': [],
                'borderWidth': 0
            }]
        }
    }

    # clearRate
    music_num = [0] * max_s_lv
    medal_num = {
        'perfect': [0] * max_s_lv,
        'fullcombo': [0] * max_s_lv,
        'hard': [0] * max_s_lv,
        'clear': [0] * max_s_lv,
        'easy': [0] * max_s_lv,
        'failed': [0] * max_s_lv,
        'no-play': [0] * max_s_lv
    }
    percentage_of_medals = {
        'perfect': [0] * max_s_lv,
        'fullcombo': [0] * max_s_lv,
        'hard': [0] * max_s_lv,
        'clear': [0] * max_s_lv,
        'easy': [0] * max_s_lv,
        'failed': [0] * max_s_lv
    }
    for s_lv in s_lv_range:
        music_list = Music.objects.filter(sran_level=s_lv)
        music_num[s_lv - 1] = len(music_list)
        for music in music_list:
            try:
                medal = Medal.objects.get(user=user, music=music)
                if medal.medal == 1:
                    medal_num['perfect'][s_lv - 1] += 1
                elif 2 <= medal.medal <= 4:
                    medal_num['fullcombo'][s_lv - 1] += 1
                elif 5 <= medal.medal <= 7:
                    try:
                        extra_option = Extra_Option.objects.get(user=user, music=music)
                        if extra_option.hard:
                            medal_num['hard'][s_lv - 1] += 1
                        else:
                            medal_num['clear'][s_lv - 1] += 1
                    except ObjectDoesNotExist:
                        medal_num['clear'][s_lv - 1] += 1
                elif medal.medal == 11:
                    medal_num['easy'][s_lv - 1] += 1
                elif 8 <= medal.medal <= 10:
                    medal_num['failed'][s_lv - 1] += 1
                else:
                    medal_num['no-play'][s_lv - 1] += 1
            except ObjectDoesNotExist:
                medal_num['no-play'][s_lv - 1] += 1

        # 各レベルのメダルの割合を計算
        percentage_of_medals['perfect'][s_lv - 1] = round(medal_num['perfect'][s_lv - 1] * 100 / music_num[s_lv - 1])
        percentage_of_medals['fullcombo'][s_lv - 1] = round(medal_num['fullcombo'][s_lv - 1] * 100 / music_num[s_lv - 1])
        percentage_of_medals['hard'][s_lv - 1] = round(medal_num['hard'][s_lv - 1] * 100 / music_num[s_lv - 1])
        percentage_of_medals['clear'][s_lv - 1] = round(medal_num['clear'][s_lv - 1] * 100 / music_num[s_lv - 1])
        percentage_of_medals['easy'][s_lv - 1] = round(medal_num['easy'][s_lv - 1] * 100 / music_num[s_lv - 1])
        percentage_of_medals['failed'][s_lv - 1] = round(medal_num['failed'][s_lv - 1] * 100 / music_num[s_lv - 1])

        chart_data['clearRate']['labels'].append("Lv" + str(s_lv))

        chart_data['clearRate']['datasets'][0]['data'].append(percentage_of_medals['perfect'][s_lv - 1])
        chart_data['clearRate']['datasets'][1]['data'].append(percentage_of_medals['fullcombo'][s_lv - 1])
        chart_data['clearRate']['datasets'][2]['data'].append(percentage_of_medals['hard'][s_lv - 1])
        chart_data['clearRate']['datasets'][3]['data'].append(percentage_of_medals['clear'][s_lv - 1])
        chart_data['clearRate']['datasets'][4]['data'].append(percentage_of_medals['easy'][s_lv - 1])
        chart_data['clearRate']['datasets'][5]['data'].append(percentage_of_medals['failed'][s_lv - 1])

        chart_data['clearRate']['datasets'][0]['backgroundColor'].append('#4a4a4a')
        chart_data['clearRate']['datasets'][1]['backgroundColor'].append('rgb(153, 207, 229)')
        chart_data['clearRate']['datasets'][2]['backgroundColor'].append('rgb(243, 192, 171)')
        chart_data['clearRate']['datasets'][3]['backgroundColor'].append('rgb(255, 242, 128)')
        chart_data['clearRate']['datasets'][4]['backgroundColor'].append('rgb(166, 227, 157)')
        chart_data['clearRate']['datasets'][5]['backgroundColor'].append('#C6C6C6')

    json_str = json.dumps(chart_data['clearRate'], ensure_ascii=False)
    return HttpResponse(json_str, content_type='application/json; charset=UTF-8')


def is_xml_http_request(req: HttpRequest) -> bool:
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
