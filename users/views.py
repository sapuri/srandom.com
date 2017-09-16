import os, zenhan, json

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404

from .models import CustomUser
from main.models import *
from .forms import *


def list(request):
    ''' ユーザーリスト '''
    # 有効なアカウントを取得
    users = CustomUser.objects.filter(is_active=True).exclude(pk=1).order_by('id')

    # ページング
    paginator = Paginator(users, 50)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context = { 'users': users }
    return render(request, 'users/list.html', context)

def mypage(request, username):
    '''
    マイページ (プロフィールページ)
    @param username: ユーザー名
    '''
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    max_s_lv = 18
    s_lv_range = range(max_s_lv, 0, -1)

    recent_medal = Medal.objects.filter(user=selected_user).order_by('-updated_at')[:20]

    context = {
        'selected_user': selected_user,
        's_lv_range': s_lv_range,
        'recent_medal': recent_medal
    }
    return render(request, 'users/mypage.html', context)

def statistics(request, username):
    '''
    統計情報
    :param str: username
    '''
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)
    activity_count = Activity.objects.filter(user=selected_user).count()

    context = {
        'selected_user': selected_user,
        'activity_count': activity_count
    }
    return render(request, 'users/statistics.html', context)

@login_required
def settings(request):
    ''' 設定 '''
    user = request.user

    # フォームの読み込み
    custom_user_form = CustomUserForm(instance=user)
    privacy_form = PrivacyForm(instance=user)
    theme_form = ThemeForm(instance=user)

    # POSTでアクセスされた場合
    if request.method == 'POST':
        if 'account' in request.POST:
            custom_user_form = CustomUserForm(request.POST, instance=user)

            if custom_user_form.is_valid():
                if custom_user_form.has_changed():
                    # 保存処理
                    if request.POST['player_name']:
                        custom_user = custom_user_form.save(commit = False) # 後でまとめて保存
                        # 全角大文字に変換
                        custom_user.player_name = zenhan.h2z(request.POST['player_name']).upper()
                        custom_user.save()  # 保存
                    if request.POST['poputomo_id']:
                        custom_user = custom_user_form.save(commit = False) # 後でまとめて保存
                        # 文字列に変換
                        custom_user.poputomo_id = str(request.POST['poputomo_id'])
                        custom_user.save()  # 保存
                    else:
                        custom_user_form.save()

        elif 'privacy' in request.POST:
            privacy_form = PrivacyForm(request.POST, instance=user)

            if privacy_form.is_valid() and privacy_form.has_changed():
                privacy_form.save()

        elif 'themes' in request.POST:
            theme_form = ThemeForm(request.POST, instance=user)

            if theme_form.is_valid() and theme_form.has_changed():
                theme_form.save()

        # メッセージを表示
        msg = '設定を更新しました！'
        messages.success(request, msg)

    context = {
        'custom_user_form': custom_user_form,
        'privacy_form': privacy_form,
        'theme_form': theme_form
    }
    return render(request, 'users/settings.html', context)

def cleardata(request, username, sran_level):
    '''
    クリア状況
    @param username: ユーザー名
    @param sran_level: S乱レベル
    '''
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    # 最大S乱レベル
    max_s_lv = 18

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    # S乱レベルID
    sran_level_id = sran_level

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level')

    # 取得曲数を取得
    music_list_count = len(music_list)

    # ページング
    paginator = Paginator(music_list, 25)
    page = request.GET.get('page')

    try:
        music_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        music_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        music_list = paginator.page(paginator.num_pages)

    # ユーザーごとにデータを取得
    medal_list = Medal.objects.filter(user=selected_user)
    bad_count_list = Bad_Count.objects.filter(user=selected_user)
    extra_option_list = Extra_Option.objects.filter(user=selected_user)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': music_list_count,
        'medal_list': medal_list,
        'bad_count_list': bad_count_list,
        'extra_option_list': extra_option_list
    }
    return render(request, 'users/cleardata.html', context)

@login_required
def deactivate(request):
    '''
    アカウント削除
    '''
    # 自ユーザーを取得
    myself = request.user

    # POSTでアクセスされた場合
    if request.method == 'POST':
        # クリアメダルを取得
        medal = Medal.objects.filter(user=myself)
        if medal:
            # メダルが存在すれば削除
            medal.delete()

        # BAD数を取得
        bad_count = Bad_Count.objects.filter(user=myself)
        if bad_count:
            # BAD数が存在すれば削除
            bad_count.delete()

        # エクストラオプションを取得
        extra_option = Extra_Option.objects.filter(user=myself)
        if extra_option:
            # エクストラオプションが存在すれば削除
            extra_option.delete()

        # アカウントを無効にする
        myself.is_active = False
        # 保存
        myself.save()

        # ログアウトページにリダイレクト
        return redirect('/auth/logout/?next=/')

    return render(request, 'users/deactivate.html')

@login_required
def download(request, file_type):
    '''
    ファイルダウンロード
    @param {string} file_type ダウンロードするファイルの種類
    '''
    if file_type == 'csv':
        if request.user.premium:
            ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # /srandom.com
            file_path = ROOT_DIR+'/csv/export/'+request.user.username+'.csv'
            try:
                response = HttpResponse(open(file_path).read(), content_type='text/csv; charset=cp932')
            except FileNotFoundError:
                raise Http404
            response['Content-Disposition'] = 'attachment; filename='+request.user.username+'.csv'
        else:
            raise PermissionDenied
        return response
    else:
        raise Http404

# ---------- API ---------- #
def get_percentage_of_clear(request, user_id):
    '''
    指定されたユーザーの各レベルのクリア率を返す
    @param {int} user_id ユーザーID
    @return {json} 各レベルのクリア率
    '''
    if request.is_ajax():
        # ユーザーを取得
        user = get_object_or_404(CustomUser, pk=user_id)

        # 権限を確認
        if user != request.user:
            if user.is_active == False or user.cleardata_privacy == 2:
                raise PermissionDenied

        max_s_lv = 18
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
                except:
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
    if (not 'user_id' in request.GET) or (not 'start' in request.GET) or (not 'stop' in request.GET):
        raise Http404()

    user_id = request.GET['user_id']
    user = get_object_or_404(CustomUser, pk=user_id)

    # 権限を確認
    if user != request.user:
        if user.is_active == False or user.cleardata_privacy == 2:
            raise PermissionDenied

    start = int(request.GET['start'])
    end = int(request.GET['stop'])

    start_datetime = datetime.fromtimestamp(start / 1000.0)
    end_datetime = datetime.fromtimestamp(end / 1000.0)
    print ('start_datetime:', start_datetime)
    print ('end_datetime:', end_datetime)

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
    if not 'user_id' in request.GET:
        raise Http404()

    user_id = request.GET['user_id']
    user = get_object_or_404(CustomUser, pk=user_id)

    max_s_lv = 18
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
                elif medal.medal >= 2 and medal.medal <= 4:
                    medal_num['fullcombo'][s_lv - 1] += 1
                elif medal.medal >= 5 and medal.medal <= 7:
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
                elif medal.medal >= 8 and medal.medal <= 10:
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
