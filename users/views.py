import zenhan

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import json

from .models import CustomUser
from main.models import Bad_Count, Medal, Extra_Option, Music
from .forms import CustomUserForm, PrivacyForm


# @login_required
# def list(request):
#     '''
#     登録ユーザー一覧
#     '''
#     # プレイヤー名を公開しているユーザーを取得
#     users = CustomUser.objects.filter(is_active=True, player_name_privacy=1)
#     context = {
#         'users': users
#     }
#     return render(request, 'users/list.html', context)

@login_required
def mypage(request, username):
    '''
    マイページ (プロフィールページ)
    @param username: ユーザー名
    '''
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    max_s_lv = 17
    s_lv_range = range(max_s_lv, 0, -1)

    recent_medal = Medal.objects.filter(user=selected_user).order_by('-updated_at')[:20]

    context = {
        'selected_user': selected_user,
        's_lv_range': s_lv_range,
        'recent_medal': recent_medal
    }
    return render(request, 'users/mypage.html', context)

@login_required
def settings(request):
    '''
    設定
    '''
    # ユーザを取得
    user = request.user

    # POSTでアクセスされた場合
    if request.method == 'POST':
        custom_user_form = CustomUserForm(request.POST, instance=user)
        privacy_form = PrivacyForm(request.POST, instance=user)

        if custom_user_form.is_valid() and privacy_form.is_valid():
            if custom_user_form.has_changed():
                # 保存処理
                if request.POST['player_name']:
                    custom_user = custom_user_form.save(commit = False) # 後でまとめて保存
                    # 全角大文字に変換
                    custom_user.player_name = zenhan.h2z(request.POST['player_name']).upper()
                    custom_user.save()         # 保存
                if request.POST['poputomo_id']:
                    custom_user = custom_user_form.save(commit = False) # 後でまとめて保存
                    # 文字列に変換
                    custom_user.poputomo_id = str(request.POST['poputomo_id'])
                    custom_user.save()         # 保存
                else:
                    custom_user_form.save()    # 保存

            if privacy_form.has_changed():
                # 保存処理
                privacy_form.save()            # 保存

            # メッセージを表示
            msg = '設定を更新しました！'
            messages.success(request, msg)

    # 通常アクセスの場合
    else:
        custom_user_form = CustomUserForm(instance=user)
        privacy_form = PrivacyForm(instance=user)

    context = {
        'custom_user_form': custom_user_form,
        'privacy_form': privacy_form
    }
    return render(request, 'users/settings.html', context)

@login_required
def cleardata(request, username, sran_level):
    '''
    クリア状況
    @param username: ユーザー名
    @param sran_level: S乱レベル
    '''
    # ユーザーを取得
    selected_user = get_object_or_404(CustomUser, username=username, is_active=True)

    # S乱レベルIDを取得
    max_s_lv = 17
    sran_level_id = max_s_lv - int(sran_level) + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level')

    # ユーザーごとにデータを取得
    medal_list = Medal.objects.filter(user=selected_user)
    bad_count_list = Bad_Count.objects.filter(user=selected_user)
    extra_option_list = Extra_Option.objects.filter(user=selected_user)

    context = {
        'selected_user': selected_user,
        'sran_level': sran_level,
        'music_list': music_list,
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

# ---------- API ---------- #
@login_required
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

        max_s_lv = 17
        s_lv_range = range(max_s_lv, 0, -1)

        music_num = [0] * max_s_lv
        clear_num = [0] * max_s_lv
        percentage_of_clear = [0] * max_s_lv

        for sran_level in s_lv_range:
            sran_level_id = max_s_lv - sran_level + 1
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
