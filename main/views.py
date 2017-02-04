import pytz
from twitter import *

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.db.models import Avg
from datetime import datetime, timedelta
import json

from .models import *
from users.models import CustomUser
from .forms import *

def index(request):
    ''' トップページ '''
    medal_num = Medal.objects.all().count()
    recent_medal = Medal.objects.all().order_by('-updated_at')[:10]
    search_form = SearchForm(request.GET)

    context = {
        'news': news,
        'medal_num': medal_num,
        'recent_medal': recent_medal,
        'search_form': search_form
    }
    return render(request, 'main/index.html', context)

def news(request):
    ''' NEWS '''
    news = News.objects.filter(status=True).order_by('-id')

    context = {
        'news': news,
    }
    return render(request, 'main/news.html', context)

def search(request):
    ''' 検索結果 '''
    def search_items(q=None):
        filter_params = {}
        if q:
            # 大文字小文字区別無しの部分一致
            filter_params['title__icontains'] = q
        return Music.objects.filter(**filter_params).order_by('level', '-sran_level', 'title')

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        if q:
            is_blank = False
            items = search_items(q=q)
        else:
            is_blank = True
            items = []
    else:
        is_blank = True
        items = []

    context = {
        'title': '{q} の検索結果'.format(q=q) if not is_blank else '楽曲検索',
        'search_form': search_form,
        'q': q,
        'items': items,
        'is_blank': is_blank
    }
    return render(request, 'main/search.html', context)

def level_select(request):
    '''
    公式難易度表: レベル選択
    '''
    # 最大レベル
    max_lv = 50

    # 最小レベル
    min_lv = 38

    # レベル 50〜38
    lv_range = range(max_lv, min_lv-1, -1)

    context = {
        'lv_range': lv_range
    }

    return render(request, 'main/level/level_select.html', context)

def level(request, level):
    '''
    難易度表
    @param level: レベル
    '''
    # 最大レベル
    max_lv = 50

    # レベルを数値に変換
    level = int(level)

    # レベルが不正なら404エラー
    if level <= 0 or level > max_lv:
        raise Http404

    # レベルIDを求める
    level_id = max_lv - level + 1

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(level=level_id).order_by('-sran_level', 'title')

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

    context = {
        'level': level,
        'music_list': music_list,
        'music_list_count': music_list_count
    }

    return render(request, 'main/level/level.html', context)

def difflist_level_select(request):
    '''
    難易度表: S乱レベル選択
    '''
    # 最大S乱レベル
    max_s_lv = 18

    s_lv_range = range(max_s_lv, 0, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/difflist_level_select.html', context)

def difflist(request, sran_level):
    '''
    難易度表
    @param sran_level: S乱レベル
    '''
    # 最大S乱レベル
    max_s_lv = 18

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    # S乱レベルIDを求める
    # sran_level_id = max_s_lv - sran_level + 1
    sran_level_id = sran_level

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

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

    context = {
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': music_list_count
    }

    return render(request, 'main/difflist.html', context)

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

    # 編集履歴を取得
    activity_list = Activity.objects.filter(music=music, user=myself).order_by('-id')

    # POSTでアクセスされた場合
    if request.method == 'POST':
        if 'save' in request.POST:
            # 記録を保存
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
            if 'tweet' in request.POST:
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
                    tweet = '『' + music.title + ' (' + music.difficulty.difficulty_short() + ')』のBAD数を' + request.POST['bad_count'] + 'に更新！ #スパランドットコム https://srandom.com/ranking/detail/' + str(music.id) + '/'
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

            # アクティビティに更新履歴を保存
            activity = Activity.objects.create(music=music, updated_at=now_datetime, user=myself)

            # リダイレクト先にメッセージを表示
            msg = music.title + ' (' + music.difficulty.difficulty_short() + ') を更新しました！'
            messages.success(request, msg)

        if 'delete' in request.POST:
            # 記録を削除
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

            # 編集履歴を削除
            activity_list.delete()

            # リダイレクト先にメッセージを表示
            msg = music.title + ' (' + music.difficulty.difficulty_short() + ') の記録を削除しました'
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
        'activity_list': activity_list
    }
    return render(request, 'main/edit.html', context)

@login_required
def ranking_level_select(request):
    '''
    ランキング: S乱レベル選択
    '''
    # 最大S乱レベル
    max_s_lv = 18

    s_lv_range = range(max_s_lv, 0, -1)

    context = {
        's_lv_range': s_lv_range
    }

    return render(request, 'main/ranking_level_select.html', context)

@login_required
def ranking(request, sran_level):
    '''
    ランキング
    @param sran_level: S乱レベル
    '''
    # 最高S乱レベル
    max_s_lv = 18

    # S乱レベルを数値に変換
    sran_level = int(sran_level)

    # S乱レベルが不正なら404エラー
    if sran_level <= 0 or sran_level > max_s_lv:
        raise Http404

    sran_level_id = sran_level

    # 対象レベルの曲を取得
    music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')

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

    context = {
        'sran_level': sran_level,
        'music_list': music_list,
        'music_list_count': music_list_count
    }

    return render(request, 'main/ranking.html', context)

def ranking_detail(request, music_id):
    '''
    ランキング: 詳細
    @param music_id: 曲ID
    '''
    # 曲を取得
    music = get_object_or_404(Music, pk=music_id)

    # 全ユーザーを取得
    users = CustomUser.objects.filter(is_active=True)

    medal_list = Medal.objects.filter(music=music)
    bad_count_list = Bad_Count.objects.filter(music=music).order_by('bad_count', 'updated_at')
    extra_option_list = Extra_Option.objects.filter(music=music)

    context = {
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

    # POSTでアクセスされた場合
    if request.method == 'POST':
        sran_level_form = Sran_LevelForm(request.POST)

        # どちらかが指定された場合
        if request.POST['sran_level_from'] or request.POST['sran_level_to']:
            # 両方指定された場合
            if request.POST['sran_level_from'] and request.POST['sran_level_to']:
                # S乱レベルIDからS乱レベルに変換
                sran_level_from = request.POST['sran_level_from']
                sran_level_to = request.POST['sran_level_to']
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
        if 'tweet' in request.POST:
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
            tweet = '今日のスパランおすすめ曲は『' + music.title + ' (' + music.difficulty.difficulty_short() + ')』です！ #スパランドットコム https://srandom.com/omikuji/'
            try:
                twitter.statuses.update(status = tweet)
                # メッセージを表示
                msg = 'おみくじの結果をツイートしました！'
                messages.success(request, msg)
            except:
                # メッセージを表示
                msg = 'おみくじの結果をツイートできませんでした'
                messages.error(request, msg)

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
            'sran_level_form': sran_level_form,
            'music': music,
            'medal': medal,
            'bad_count': bad_count,
            'extra_option': extra_option
        }
        return render(request, 'main/omikuji.html', context)
    except:
        context = {
            'sran_level_form': sran_level_form
        }
        return render(request, 'main/omikuji.html', context)

def premium(request):
    ''' プレミアムユーザー '''
    return render(request, 'main/premium.html')

# ---------- API ---------- #
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
            medal = Medal.objects.get(music=music_id, user=user)
        except:
            medal = None

        if medal:
            # 更新日時 (日本時間 UTC+9 に変換)
            updated_at = medal.updated_at + timedelta(hours=9)

            context = {
                'is_active': True,
                'year': updated_at.year,
                'month': updated_at.month,
                'day': updated_at.day,
                'hour': updated_at.hour,
                'minute': updated_at.minute,
                'second': updated_at.second
            }
        else:
            context = {
                'is_active': False
            }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')

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
            # BAD数の平均を計算 (小数点以下四捨五入)
            bad_count_avg = round(bad_count_list.aggregate(Avg('bad_count'))['bad_count__avg'])

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

def get_folder_lamp(request, level):
    '''
    指定されたレベルのフォルダランプを返す
    @param {int} level レベル
    @param {bool} ?is_srandom S乱レベルかどうか
    @param {int} ?user_id ユーザーID
    @return {json} フォルダランプ
    '''
    if request.is_ajax():
        if request.user.is_authenticated():
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

            # 指定されたレベルの曲を取得
            level = int(level)
            if request.GET['is_srandom'] == 'true':
                max_lv = 18
                # level = max_lv - level + 1
                music_list = Music.objects.filter(sran_level=level)
            else:
                max_lv = 50
                level = max_lv - level + 1
                music_list = Music.objects.filter(level=level)

            medal_max = 0
            easy_flg = False
            hard_flg = True
            for music in music_list:
                # メダルを取得
                try:
                    medal = Medal.objects.get(music=music.id, user=user)
                except ObjectDoesNotExist:
                    medal = None

                # 1曲でも未プレイがあれば未プレイで決定
                if not medal or medal.medal == 12:
                    medal_max = 0
                    easy_flg = False
                    hard_flg = False
                    break

                # イージーメダルの場合
                if medal.medal == 11:
                    easy_flg = True

                # クリアメダルの場合はハード判定
                elif medal.medal >= 5 and medal.medal <=7 and hard_flg:
                    # 1曲でも未ハードなら未ハードで確定
                    try:
                        extra_option = Extra_Option.objects.get(music=medal.music, user=user)
                        if not extra_option.hard:
                            hard_flg = False
                    except ObjectDoesNotExist:
                        hard_flg = False

                # メダルの最大値を更新
                if medal_max < medal.medal:
                    medal_max = medal.medal

            # 1曲でもイージーメダルだった場合
            if easy_flg:
                if medal_max >= 8 and medal_max <= 10:
                    folder_lamp = 'failed'
                else:
                    folder_lamp = 'easy-cleared'

            # 全曲プレイ済みの場合
            elif medal_max:
                if medal_max == 1:
                    folder_lamp = 'perfect'
                elif medal_max >= 2 and medal_max <= 4:
                    folder_lamp = 'fullcombo'
                elif medal_max >= 5 and medal_max <= 7:
                    if hard_flg:
                        folder_lamp = 'hard-cleared'
                    else:
                        folder_lamp = 'cleared'
                elif medal_max >= 8 and medal_max <= 10:
                    folder_lamp = 'failed'

            # 未プレイの場合
            else:
                folder_lamp = 'no-play'
        else:
            # 未認証ユーザーの場合
            folder_lamp = 'no-play'

        context = {
            'folder_lamp': folder_lamp
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')
