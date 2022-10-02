from random import choice

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from twitter import Twitter, OAuth

from main.forms import Sran_LevelForm
from main.models import Music, Medal, Bad_Count, Extra_Option
from srandom import settings


@login_required
def omikuji(request: HttpRequest) -> HttpResponse:
    """
    スパランおみくじ
    指定されたS乱レベルの範囲の曲からランダムで選曲
    """

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
                    pks = Music.objects.filter(sran_level__level__range=(sran_level_from, sran_level_to)).values_list('pk', flat=True)
                    music = Music.objects.get(pk=choice(pks))
                else:
                    # to から from までの範囲でランダムで1曲取得
                    pks = Music.objects.filter(sran_level__level__range=(sran_level_to, sran_level_from)).values_list('pk', flat=True)
                    music = Music.objects.get(pk=choice(pks))
            # from のみ指定された場合
            elif request.POST['sran_level_from']:
                # 指定されたS乱レベルの曲からランダムで1曲取得
                pks = Music.objects.filter(sran_level=request.POST['sran_level_from']).values_list('pk', flat=True)
                music = Music.objects.get(pk=choice(pks))
            # to のみ指定された場合
            else:
                # 指定されたS乱レベルの曲からランダムで1曲取得
                pks = Music.objects.filter(sran_level=request.POST['sran_level_to']).values_list('pk', flat=True)
                music = Music.objects.get(pk=choice(pks))
        # 何も指定されなかった場合
        else:
            # 全ての曲からランダムで1曲取得
            pks = Music.objects.values_list('pk', flat=True)
            music = Music.objects.get(pk=choice(pks))

        # おみくじ結果をツイート
        if 'tweet' in request.POST:
            # 自ユーザーのtwitter情報を取得
            social = myself.social_auth.get(provider='twitter')
            # パラメータを取得
            oauth_token = social.extra_data['access_token']['oauth_token']
            oauth_secret = social.extra_data['access_token']['oauth_token_secret']
            # Twitterクラスを作成
            twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET))
            # ツイート
            tweet = f'今日のスパランおすすめ曲は『{music.title} ({music.difficulty.difficulty_short()})』です！ https://srandom.com/omikuji/ #スパランドットコム'
            try:
                twitter.statuses.update(status=tweet)
                # メッセージを表示
                msg = 'おみくじの結果をツイートしました！'
                messages.success(request, msg)
            except Exception:
                # メッセージを表示
                msg = 'おみくじの結果をツイートできませんでした'
                messages.error(request, msg)

    try:
        try:
            medal = Medal.objects.get(user=myself, music=music)
        except Exception:
            medal = None
        try:
            bad_count = Bad_Count.objects.get(user=myself, music=music)
        except Exception:
            bad_count = None
        try:
            extra_option = Extra_Option.objects.get(user=myself, music=music)
        except Exception:
            extra_option = None
        context = {
            'sran_level_form': sran_level_form,
            'music': music,
            'medal': medal,
            'bad_count': bad_count,
            'extra_option': extra_option
        }
        return render(request, 'main/omikuji.html', context)
    except Exception:
        context = {
            'sran_level_form': sran_level_form
        }
        return render(request, 'main/omikuji.html', context)
