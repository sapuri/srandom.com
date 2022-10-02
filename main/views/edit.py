from datetime import datetime

import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from twitter import Twitter, OAuth

from main.forms import MedalForm, Bad_CountForm, Extra_OptionForm
from main.models import Activity, Medal, Bad_Count, Extra_Option, Music
from srandom import settings


@login_required
def edit(request: HttpRequest, music_id: int) -> HttpResponse:
    """ 指定された曲の記録を編集 """

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
            except Exception:
                # メダルが存在しなければ新規追加
                medal_form = MedalForm(request.POST)

            if medal_form.is_valid():
                if medal_form.has_changed():
                    # 保存処理
                    medal = medal_form.save(commit=False)  # 後でまとめて保存
                    medal.music = music  # 曲
                    medal.user = myself  # ユーザー
                    medal.updated_at = now_datetime  # 現在日時
                    medal.save()  # 保存

            # BAD数を登録
            try:
                # BAD数が存在すれば呼び出して更新
                bad_count = Bad_Count.objects.get(music=music_id, user=myself)
                bad_count_form = Bad_CountForm(request.POST, instance=bad_count)
            except Exception:
                # BAD数が存在しなければ新規追加
                bad_count_form = Bad_CountForm(request.POST)

            if medal_form.is_valid():
                if bad_count_form.has_changed():
                    # 保存処理
                    bad_count = bad_count_form.save(commit=False)  # 後でまとめて保存
                    bad_count.music = music  # 曲
                    bad_count.user = myself  # ユーザー
                    bad_count.updated_at = now_datetime  # 現在日時
                    bad_count.save()  # 保存

            # エクストラオプションを記録
            try:
                # エクストラオプションが存在すれば呼び出して更新
                extra_option = Extra_Option.objects.get(music=music_id, user=myself)
                extra_option_form = Extra_OptionForm(request.POST, instance=extra_option)

                if extra_option_form.has_changed():
                    # BooleanFieldの場合、チェックを入れないとvalidにならないのでis_validでTrue/Falseを判定
                    if extra_option_form.is_valid():
                        # チェックされていればTrueを設定
                        extra_option = extra_option_form.save(commit=False)  # 後でまとめて保存
                    else:
                        # チェックされていなければFalseを設定
                        extra_option.hard = 0  # False

                    # 保存処理
                    extra_option.music = music  # 曲
                    extra_option.user = myself  # ユーザー
                    extra_option.updated_at = now_datetime  # 現在日時
                    extra_option.save()  # 保存
            except Exception:
                # エクストラオプションが存在しなければ新規追加
                extra_option_form = Extra_OptionForm(request.POST)

                if extra_option_form.is_valid():
                    # 保存処理
                    extra_option = extra_option_form.save(commit=False)  # 後でまとめて保存
                    extra_option.music = music  # 曲
                    extra_option.user = myself  # ユーザー
                    extra_option.updated_at = now_datetime  # 現在日時
                    extra_option.save()  # 保存

            # 更新をツイート
            if 'tweet' in request.POST:
                # 自ユーザーのtwitter情報を取得
                social = myself.social_auth.get(provider='twitter')
                # パラメータを取得
                oauth_token = social.extra_data['access_token']['oauth_token']
                oauth_secret = social.extra_data['access_token']['oauth_token_secret']
                # Twitterクラスを作成
                twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET))
                # ツイート
                if request.POST['bad_count']:
                    tweet = '『' + music.title + ' (' + music.difficulty.difficulty_short() + ')』のBAD数を' + request.POST[
                        'bad_count'] + 'に更新！ https://srandom.com/ranking/detail/' + str(music.id) + '/ #スパランドットコム'
                    try:
                        twitter.statuses.update(status=tweet)
                        # リダイレクト先にメッセージを表示
                        msg = '更新内容をツイートしました！'
                        messages.success(request, msg)
                    except Exception:
                        # リダイレクト先にメッセージを表示
                        msg = '更新内容をツイートできませんでした'
                        messages.error(request, msg)
                else:
                    # リダイレクト先にメッセージを表示
                    msg = '更新内容をツイートするにはBAD数の入力が必要です'
                    messages.error(request, msg)

            # アクティビティに更新履歴を保存
            Activity.objects.create(music=music, updated_at=now_datetime, user=myself)

            # リダイレクト先にメッセージを表示
            msg = f'{music.title} ({music.difficulty.difficulty_short()}) を更新しました！'
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
            msg = f'{music.title} ({music.difficulty.difficulty_short()}) の記録を削除しました'
            messages.success(request, msg)

        if 'next' in request.GET:
            return redirect(request.GET['next'])

    # 通常アクセスの場合
    else:
        try:
            # メダルが存在すれば既存のデータを初期値に設定
            medal = Medal.objects.get(music=music_id, user=myself)
            medal_form = MedalForm(instance=medal)
        except Exception:
            # メダルが存在しなければ初期値を未プレイに設定
            medal_form = MedalForm(initial={
                'medal': 12  # 未プレイ
            })

        try:
            # BAD数が存在すれば既存のデータを初期値に設定
            bad_count = Bad_Count.objects.get(music=music_id, user=myself)
            bad_count_form = Bad_CountForm(instance=bad_count)
        except Exception:
            # BAD数が存在しなければ初期値を設定しない
            bad_count_form = Bad_CountForm()

        try:
            # エクストラオプションが存在すれば既存のデータを初期値に設定
            extra_option = Extra_Option.objects.get(music=music_id, user=myself)
            extra_option_form = Extra_OptionForm(instance=extra_option)
        except Exception:
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
