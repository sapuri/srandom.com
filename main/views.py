import pytz
from twitter import *

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from datetime import datetime
import json

from .models import Music, Medal, Bad_Count, Extra_Option
from users.models import CustomUser
from .forms import Sran_LevelForm, MedalForm, Bad_CountForm, Extra_OptionForm

def index(request):
    '''
    トップページ
    '''
    myself = request.user

    context = {
        'myself': myself
    }
    return render(request, 'main/index.html', context)

@login_required
def level_select(request):
    '''
    公式難易度表: レベル選択
    '''
    myself = request.user

    # レベル 50〜38
    lv_range = range(50, 37, -1)

    context = {
        'myself': myself,
        'lv_range': lv_range
    }

    return render(request, 'main/level/level_select.html', context)

@login_required
def level(request, level):
    '''
    難易度表
    @param level: レベル
    '''
    myself = request.user

    # S乱レベルIDを取得
    max_lv = 50

    # S乱レベルを数値に変換
    level = int(level)

    # S乱レベルが不正なら404エラー
    if level <= 0 or level > max_lv:
        raise Http404

    # S乱レベルIDを求める
    level_id = max_lv - level + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(level=level_id).order_by('sran_level', 'title')

    context = {
        'myself': myself,
        'level': level,
        'music_list': music_list
    }

    return render(request, 'main/level/level.html', context)

@login_required
def difflist_level_select(request):
    '''
    難易度表: S乱レベル選択
    '''
    myself = request.user

    # S乱レベル 17〜1
    s_lv_range = range(17, 0, -1)

    context = {
        'myself': myself,
        's_lv_range': s_lv_range
    }

    return render(request, 'main/difflist_level_select.html', context)

@login_required
def difflist(request, sran_level):
    '''
    難易度表
    @param sran_level: S乱レベル
    '''
    myself = request.user

    # S乱レベルIDを取得
    max_s_lv = 17

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    # S乱レベルIDを求める
    sran_level_id = max_s_lv - sran_level + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

    context = {
        'myself': myself,
        'sran_level': sran_level,
        'music_list': music_list
    }

    return render(request, 'main/difflist.html', context)

# @login_required
# def difflist_all(request):
#     '''
#     難易度表(全レベル)
#     '''
#     myself = request.user
#
#     # ユーザごとにデータを取得
#     music_list = Music.objects.order_by('level', 'title')
#     s_lv_range = range(17, 0, -1)
#
#     context = {
#         'myself': myself,
#         'music_list': music_list,
#         's_lv_range': s_lv_range
#     }
#     return render(request, 'main/difflist_all.html', context)

# 記録編集
@login_required
def edit(request, music_id):
    '''
    指定された曲の記録を編集
    @param music_id: 曲ID
    '''
    # 曲を取得
    music = get_object_or_404(Music, pk=music_id)

    # ユーザーを取得
    myself = request.user

    # POSTでアクセスされた場合
    if request.method == 'POST':
        # 日本の日時を取得
        now_datetime = datetime.now(pytz.timezone('Asia/Tokyo'))

        # クリアメダルを登録
        try:
            # メダルが存在すれば呼び出して更新
            medal = Medal.objects.get(music=music_id, user=myself)
            medal_form = MedalForm(request.POST, instance=medal)
        except:
            # メダルが存在しなければ新規追加
            medal_form = MedalForm(request.POST)

        if medal_form.is_valid():
            if medal_form.has_changed():
                # 保存処理
                medal = medal_form.save(commit = False)                 # 後でまとめて保存
                medal.music = music                                     # 曲
                medal.user = myself                                     # ユーザー
                medal.updated_at = now_datetime                         # 現在日時
                medal.save()                                            # 保存

        # BAD数を登録
        try:
            # BAD数が存在すれば呼び出して更新
            bad_count = Bad_Count.objects.get(music=music_id, user=myself)
            bad_count_form = Bad_CountForm(request.POST, instance=bad_count)
        except:
            # BAD数が存在しなければ新規追加
            bad_count_form = Bad_CountForm(request.POST)

        if medal_form.is_valid():
            if bad_count_form.has_changed():
                # 保存処理
                bad_count = bad_count_form.save(commit = False)         # 後でまとめて保存
                bad_count.music = music                                 # 曲
                bad_count.user = myself                                 # ユーザー
                bad_count.updated_at = now_datetime                     # 現在日時
                bad_count.save()                                        # 保存

        # エクストラオプションを記録
        try:
            # エクストラオプションが存在すれば呼び出して更新
            extra_option = Extra_Option.objects.get(music=music_id, user=myself)
            extra_option_form = Extra_OptionForm(request.POST, instance=extra_option)

            if extra_option_form.has_changed():
                # BooleanFieldの場合、チェックを入れないとvalidにならないのでis_validでTrue/Falseを判定
                if extra_option_form.is_valid():
                    # チェックされていればTrueを設定
                    extra_option = extra_option_form.save(commit = False)   # 後でまとめて保存
                else:
                    # チェックされていなければFalseを設定
                    extra_option.hard = 0   # False

                # 保存処理
                extra_option.music = music                              # 曲
                extra_option.user = myself                              # ユーザー
                extra_option.updated_at = now_datetime                  # 現在日時
                extra_option.save()                                     # 保存
        except:
            # エクストラオプションが存在しなければ新規追加
            extra_option_form = Extra_OptionForm(request.POST)

            if extra_option_form.is_valid():
                # 保存処理
                extra_option = extra_option_form.save(commit = False)   # 後でまとめて保存
                extra_option.music = music                              # 曲
                extra_option.user = myself                              # ユーザー
                extra_option.updated_at = now_datetime                  # 現在日時
                extra_option.save()                                     # 保存

        # 更新をツイート
        try:
            if request.POST['tweet']:
                # 自ユーザーのtwitter情報を取得
                social = myself.social_auth.get(provider='twitter')
                # パラメータを取得
                oauth_token = social.extra_data['access_token']['oauth_token']
                oauth_secret = social.extra_data['access_token']['oauth_token_secret']
                CONSUMER_KEY = 'Pwyx6QZgunJsbrArLub7pNKwu'
                CONSUMER_SECRET = 'D7J4xAE7aXLrqGyaKy8adpxtU1rrAEuZy8MaRUw3GUUzG6BLeO'
                # Twitterクラスを作成
                twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
                # ツイート
                if request.POST['bad_count']:
                    tweet = '『' + music.title + ' (' + music.difficulty.difficulty_short() + ')』のBAD数を' + request.POST['bad_count'] + 'に更新！ #スパランドットコム http://srandom.com/ranking/detail/' + str(music.id) + '/'
                    try:
                        twitter.statuses.update(status = tweet)
                        # リダイレクト先にメッセージを表示
                        msg = '更新内容をツイートしました！'
                        messages.success(request, msg)
                    except:
                        # リダイレクト先にメッセージを表示
                        msg = '更新内容をツイートできませんでした'
                        messages.error(request, msg)
                else:
                    # リダイレクト先にメッセージを表示
                    msg = '更新内容をツイートするにはBAD数の入力が必要です'
                    messages.error(request, msg)

        # チェックされなかった場合はパス
        except KeyError:
            pass

        # リダイレクト先にメッセージを表示
        msg = music.title + ' (' + music.difficulty.difficulty_short() + ') を更新しました！'
        messages.success(request, msg)

        if 'next' in request.GET:
            return redirect(request.GET['next'])

    # 通常アクセスの場合
    else:
        try:
            # メダルが存在すれば既存のデータを初期値に設定
            medal = Medal.objects.get(music=music_id, user=myself)
            medal_form = MedalForm(instance=medal)
        except:
            # メダルが存在しなければ初期値を未プレイに設定
            medal_form = MedalForm(initial = {
                'medal': 12     # 未プレイ
            })

        try:
            # BAD数が存在すれば既存のデータを初期値に設定
            bad_count = Bad_Count.objects.get(music=music_id, user=myself)
            bad_count_form = Bad_CountForm(instance=bad_count)
        except:
            # BAD数が存在しなければ初期値を設定しない
            bad_count_form = Bad_CountForm()

        try:
            # エクストラオプションが存在すれば既存のデータを初期値に設定
            extra_option = Extra_Option.objects.get(music=music_id, user=myself)
            extra_option_form = Extra_OptionForm(instance=extra_option)
        except:
            # エクストラオプションが存在しなければ初期値を設定しない
            extra_option_form = Extra_OptionForm()

    context = {
        'music': music,
        'medal_form': medal_form,
        'bad_count_form': bad_count_form,
        'extra_option_form': extra_option_form,
        'myself': myself,
    }
    return render(request, 'main/edit.html', context)

# 記録削除
@login_required
def delete(request, music_id):
    '''
    指定された曲の記録を削除
    @param music_id: 曲ID
    '''
    # 曲を取得
    music = get_object_or_404(Music, pk=music_id)

    # ユーザーを取得
    myself = request.user

    # POSTでアクセスされた場合
    if request.method == 'POST':
        # クリアメダルを取得
        medal = Medal.objects.filter(music=music_id, user=myself)
        if medal:
            # メダルが存在すれば削除
            medal.delete()

        # BAD数を取得
        bad_count = Bad_Count.objects.filter(music=music_id, user=myself)
        if bad_count:
            # BAD数が存在すれば削除
            bad_count.delete()

        # エクストラオプションを取得
        extra_option = Extra_Option.objects.filter(music=music_id, user=myself)
        if extra_option:
            # エクストラオプションが存在すれば削除
            extra_option.delete()

        # リダイレクト先にメッセージを表示
        msg = music.title + ' (' + music.difficulty.difficulty_short() + ') の記録を削除しました'
        messages.success(request, msg)

        if 'next' in request.GET:
            return redirect(request.GET['next'])

    # 通常アクセスの場合
    else:
        context = {
            'music': music,
            'myself': myself
        }
        return render(request, 'main/delete.html', context)

@login_required
def ranking_level_select(request):
    '''
    ランキング: S乱レベル選択
    '''
    myself = request.user

    # S乱レベル 17〜1
    s_lv_range = range(17, 0, -1)

    context = {
        'myself': myself,
        's_lv_range': s_lv_range
    }

    return render(request, 'main/ranking_level_select.html', context)

@login_required
def ranking(request, sran_level):
    '''
    ランキング
    @param sran_level: S乱レベル
    '''
    myself = request.user

    # 最高S乱レベル
    max_s_lv = 17

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    sran_level_id = max_s_lv - sran_level + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

    context = {
        'myself': myself,
        'sran_level': sran_level,
        'music_list': music_list
    }

    return render(request, 'main/ranking.html', context)

@login_required
def ranking_detail(request, music_id):
    '''
    ランキング: 詳細
    @param music_id: 曲ID
    '''
    # 曲を取得
    music = get_object_or_404(Music, pk=music_id)

    # 自ユーザーを取得
    myself = request.user

    # 全ユーザーを取得
    users = CustomUser.objects.filter(is_active=True)

    medal_list = Medal.objects.filter(music=music)
    bad_count_list = Bad_Count.objects.filter(music=music).order_by('bad_count')
    extra_option_list = Extra_Option.objects.filter(music=music)

    context = {
        'myself': myself,
        'users': users,
        'music': music,
        'medal_list': medal_list,
        'bad_count_list': bad_count_list,
        'extra_option_list': extra_option_list
    }

    return render(request, 'main/ranking_detail.html', context)

@login_required
def omikuji(request):
    '''
    スパランおみくじ
    指定されたS乱レベルの範囲の曲からランダムで選曲
    '''
    myself = request.user
    sran_level_form = Sran_LevelForm()
    max_s_lv = 17   # 最大S乱レベル

    # POSTでアクセスされた場合
    if request.method == 'POST':
        # どちらかが指定された場合
        if request.POST['sran_level_from'] or request.POST['sran_level_to']:
            # 両方指定された場合
            if request.POST['sran_level_from'] and request.POST['sran_level_to']:
                # S乱レベルIDからS乱レベルに変換
                sran_level_from = max_s_lv - int(request.POST['sran_level_from']) + 1
                sran_level_to = max_s_lv - int(request.POST['sran_level_to']) + 1
                if sran_level_from <= sran_level_to:
                    # from から to までの範囲でランダムで1曲取得
                    music = Music.objects.filter(sran_level__level__range=(sran_level_from, sran_level_to)).order_by('?')[0]
                else:
                    # to から from までの範囲でランダムで1曲取得
                    music = Music.objects.filter(sran_level__level__range=(sran_level_to, sran_level_from)).order_by('?')[0]
            # from のみ指定された場合
            elif request.POST['sran_level_from']:
                # 指定されたS乱レベルの曲からランダムで1曲取得
                music = Music.objects.filter(sran_level=request.POST['sran_level_from']).order_by('?')[0]
            # to のみ指定された場合
            else:
                # 指定されたS乱レベルの曲からランダムで1曲取得
                music = Music.objects.filter(sran_level=request.POST['sran_level_to']).order_by('?')[0]
        # 何も指定されなかった場合
        else:
            # 全ての曲からランダムで1曲取得
            music = Music.objects.all().order_by('?')[0]

        # おみくじ結果をツイート
        try:
            if request.POST['tweet']:
                # 自ユーザーのtwitter情報を取得
                social = myself.social_auth.get(provider='twitter')
                # パラメータを取得
                oauth_token = social.extra_data['access_token']['oauth_token']
                oauth_secret = social.extra_data['access_token']['oauth_token_secret']
                CONSUMER_KEY = 'Pwyx6QZgunJsbrArLub7pNKwu'
                CONSUMER_SECRET = 'D7J4xAE7aXLrqGyaKy8adpxtU1rrAEuZy8MaRUw3GUUzG6BLeO'
                # Twitterクラスを作成
                twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
                # ツイート
                tweet = '今日のスパランおすすめ曲は『' + music.title + ' (' + music.difficulty.difficulty_short() + ')』です！ #スパランドットコム http://srandom.com/omikuji/'
                try:
                    twitter.statuses.update(status = tweet)
                    # メッセージを表示
                    msg = 'おみくじの結果をツイートしました！'
                    messages.success(request, msg)
                except:
                    # メッセージを表示
                    msg = 'おみくじの結果をツイートできませんでした'
                    messages.error(request, msg)

        # チェックされなかった場合はパス
        except KeyError:
            pass

    try:
        try:
            medal = Medal.objects.get(user=myself, music=music)
        except:
            medal = None
        try:
            bad_count = Bad_Count.objects.get(user=myself, music=music)
        except:
            bad_count = None
        try:
            extra_option = Extra_Option.objects.get(user=myself, music=music)
        except:
            extra_option = None
        context = {
            'myself': myself,
            'sran_level_form': sran_level_form,
            'music': music,
            'medal': medal,
            'bad_count': bad_count,
            'extra_option': extra_option
        }
        return render(request, 'main/omikuji.html', context)
    except:
        context = {
            'myself': myself,
            'sran_level_form': sran_level_form
        }
        return render(request, 'main/omikuji.html', context)

@login_required
def premium(request):
    '''
    プレミアムユーザー登録ページ
    '''
    myself = request.user

    context = {
        'myself': myself
    }
    return render(request, 'main/premium.html', context)

# ---------- API ---------- #
@login_required
def get_clear_status(request, music_id):
    '''
    指定された曲のクリア状況を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} クリア状況
    '''
    if request.is_ajax():
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if user.is_active == False or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        # BAD数を取得
        try:
            bad_count = Bad_Count.objects.get(music=music_id, user=user)
            bad_count = bad_count.bad_count
        except:
            bad_count = None

        # メダルを取得
        try:
            medal = Medal.objects.get(music=music_id, user=user)
            medal = medal.medal
        except:
            medal = None

        # エクストラオプションを取得
        try:
            extra_option = Extra_Option.objects.get(music=music_id, user=user)
        except:
            extra_option = None

        if medal:
            if medal == 1 and bad_count == 0:
                clear_status = 'perfect'
            elif (medal == 2 or medal == 3 or medal == 4) and bad_count == 0:
                clear_status = 'fullcombo'
            elif (medal >= 1 and medal <= 7) and extra_option and extra_option.hard:
                clear_status = 'hard-cleared'
            elif medal == 5 or medal == 6 or medal == 7:
                clear_status = 'cleared'
            elif medal == 8 or medal == 9 or medal == 10:
                clear_status = 'failed'
            elif medal == 11:
                clear_status = 'easy-cleared'
            else:
                clear_status = 'no-play'
        else:
            clear_status = 'no-play'

        context = {
            'clear_status': clear_status
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_bad_count(request, music_id):
    '''
    指定された曲のBAD数を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} BAD数
    '''
    if request.is_ajax():
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if user.is_active == False or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            bad_count = Bad_Count.objects.get(music=music_id, user=user)
            bad_count = bad_count.bad_count
        except:
            bad_count = None

        context = {
            'bad_count': bad_count
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_medal(request, music_id):
    '''
    指定された曲のメダルを返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} メダル(int)
    '''
    if request.is_ajax():
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if user.is_active == False or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            medal = Medal.objects.get(music=music_id, user=user)
            medal = medal.medal
        except:
            medal = None

        context = {
            'medal': medal
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_latest_updated_at(request, music_id):
    '''
    指定された曲の最新の更新日時を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} 更新日時
    '''
    if request.is_ajax():
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if user.is_active == False or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            bad_count = Bad_Count.objects.get(music=music_id, user=user)
        except:
            bad_count = None
        try:
            medal = Medal.objects.get(music=music_id, user=user)
        except:
            medal = None
        try:
            extra_option = Extra_Option.objects.get(music=music_id, user=user)
        except:
            extra_option = None

        # 最新の更新日時を取得
        if bad_count and medal and extra_option:
            bad_count_updated_at = bad_count.updated_at
            medal_updated_at = medal.updated_at
            extra_option_updated_at = extra_option.updated_at
            latest = max(bad_count_updated_at, medal_updated_at, extra_option_updated_at)
        elif bad_count and medal:
            bad_count_updated_at = bad_count.updated_at
            medal_updated_at = medal.updated_at
            extra_option_updated_at = None
            latest = max(bad_count_updated_at, medal_updated_at)
        elif medal and extra_option:
            bad_count_updated_at = None
            medal_updated_at = medal.updated_at
            extra_option_updated_at = extra_option.updated_at
            latest = max(medal_updated_at, extra_option_updated_at)
        elif bad_count:
            bad_count_updated_at = bad_count.updated_at
            medal_updated_at = None
            extra_option_updated_at = None
            latest = bad_count_updated_at
        elif medal:
            bad_count_updated_at = None
            medal_updated_at = medal.updated_at
            extra_option_updated_at = None
            latest = medal_updated_at
        elif extra_option:
            bad_count_updated_at = None
            medal_updated_at = None
            extra_option_updated_at = extra_option.updated_at
            latest = extra_option_updated_at
        else:
            bad_count_updated_at = None
            medal_updated_at = None
            extra_option_updated_at = None
            latest = None

        if latest:
            context = {
                'is_active': True,
                'year': latest.year,
                'month': latest.month,
                'day': latest.day,
                'hour': latest.hour + 9,    # UTC+9
                'minute': latest.minute,
                'second': latest.second
            }
        else:
            context = {
                'is_active': False
            }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_bad_count_avg(request, music_id):
    '''
    指定された曲の平均BAD数を返す
    @param {int} music_id 曲ID
    @return {json} 平均BAD数
    '''
    if request.is_ajax():
        bad_count_list = Bad_Count.objects.filter(music=music_id)
        if not bad_count_list:
            bad_count_avg = -1
        else:
            bad_count_sum = 0   # BAD数の合計
            bad_count_num = 0   # BAD数の個数

            for bad_count in bad_count_list:
                bad_count_sum += bad_count.int()
                bad_count_num += 1

            # BAD数の平均を計算 (小数点以下四捨五入)
            bad_count_avg = round(bad_count_sum / bad_count_num)

        context = {
            'bad_count_avg': bad_count_avg
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_myrank(request, music_id):
    '''
    指定された曲の順位を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} 順位
    '''
    if request.is_ajax():
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if user.is_active == False or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        # 該当曲のBAD数リストを取得（昇順）
        bad_count_list = Bad_Count.objects.filter(music=music_id).order_by('bad_count')

        bad_count_num = 0   # BAD数の個数
        bad_count_now = -1  # 現在のBAD数
        myrank = 0          # 自ランク
        found = False       # BAD数を登録済であればTrueを返す

        for bad_count in bad_count_list:
            bad_count_before = bad_count_now
            bad_count_now = bad_count.bad_count

            # BAD数が前後で重複した場合
            if bad_count_now == bad_count_before:
                # 指定されたユーザーの記録が見つかれば myrank にランクを格納
                if bad_count.user.id == user.id:
                    found = True
                    myrank = tmp_rank

                bad_count_num += 1

            # BAD数が重複しなかった場合
            else:
                bad_count_num += 1

                # 一時ランクを更新
                tmp_rank = bad_count_num

                # 自分の記録が見つかれば myrank にランクを格納
                if bad_count.user.id == user.id:
                    found = True
                    myrank = bad_count_num

        context = {
            'myrank': myrank,
            'bad_count_num': bad_count_num
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

@login_required
def get_medal_count(request, music_id):
    '''
    指定された曲の各メダルの枚数を返す
    @param {int} music_id 曲ID
    @return {json} 各メダルの枚数, メダルの総数
    '''
    if request.is_ajax():
        medal_count_list = []
        medal_count_total = 0
        for i in range(1, 12):
            medal_count = Medal.objects.filter(medal=i, music=music_id).count()
            medal_count_list.append(medal_count)
            medal_count_total += medal_count

        context = {
            'medal_count_list': medal_count_list,
            'medal_count_total': medal_count_total
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')
