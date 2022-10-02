import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Avg
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404

from main.models import Bad_Count, Medal, Extra_Option, Music
from users.models import CustomUser


def get_clear_status(request, music_id):
    """
    指定された曲のクリア状況を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} クリア状況
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if not user.is_active or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        # BAD数を取得
        try:
            bad_count = Bad_Count.objects.get(music=music_id, user=user)
            bad_count = bad_count.bad_count
        except Exception:
            bad_count = None

        # メダルを取得
        try:
            medal = Medal.objects.get(music=music_id, user=user)
            medal = medal.medal
        except Exception:
            medal = None

        # エクストラオプションを取得
        try:
            extra_option = Extra_Option.objects.get(music=music_id, user=user)
        except Exception:
            extra_option = None

        if medal:
            if medal == 1 and bad_count == 0:
                clear_status = 'perfect'
            elif (medal == 2 or medal == 3 or medal == 4) and bad_count == 0:
                clear_status = 'fullcombo'
            elif (1 <= medal <= 7) and extra_option and extra_option.hard:
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
    """
    指定された曲のBAD数を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} BAD数
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if not user.is_active or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            bad_count = Bad_Count.objects.get(music=music_id, user=user)
            bad_count = bad_count.bad_count
        except Exception:
            bad_count = None

        context = {
            'bad_count': bad_count
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')


def get_medal(request, music_id):
    """
    指定された曲のメダルを返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} メダル(int)
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if not user.is_active or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            medal = Medal.objects.get(music=music_id, user=user)
            medal = medal.medal
        except Exception:
            medal = None

        context = {
            'medal': medal
        }

        json_str = json.dumps(context, ensure_ascii=False)
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8')
    else:
        return HttpResponse('invalid access')


def get_latest_updated_at(request, music_id):
    """
    指定された曲の最新の更新日時を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} 更新日時
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if not user.is_active or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        try:
            medal = Medal.objects.get(music=music_id, user=user)
        except Exception:
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
    """
    指定された曲の平均BAD数を返す
    @param {int} music_id 曲ID
    @return {json} 平均BAD数
    """
    if is_xml_http_request(request):
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
    """
    指定された曲の順位を返す
    @param {int} music_id 曲ID
    @param {int} ?user_id ユーザーID
    @return {json} 順位
    """
    if is_xml_http_request(request):
        # ユーザーを取得
        try:
            # クエリでユーザーIDが指定されればそのユーザーを取得
            user_id = request.GET['user_id']
            user = get_object_or_404(CustomUser, pk=user_id)

            # 権限を確認
            if user != request.user:
                if not user.is_active or user.cleardata_privacy == 2:
                    raise PermissionDenied
        except KeyError:
            user = request.user

        # 該当曲のBAD数リストを取得（昇順）
        bad_count_list = Bad_Count.objects.filter(music=music_id).order_by('bad_count')

        bad_count_num = 0  # BAD数の個数
        bad_count_now = -1  # 現在のBAD数
        myrank = 0  # 自ランク
        tmp_rank = 0

        for bad_count in bad_count_list:
            bad_count_before = bad_count_now
            bad_count_now = bad_count.bad_count

            # BAD数が前後で重複した場合
            if bad_count_now == bad_count_before:
                # 指定されたユーザーの記録が見つかれば myrank にランクを格納
                if bad_count.user.id == user.id:
                    myrank = tmp_rank

                bad_count_num += 1

            # BAD数が重複しなかった場合
            else:
                bad_count_num += 1

                # 一時ランクを更新
                tmp_rank = bad_count_num

                # 自分の記録が見つかれば myrank にランクを格納
                if bad_count.user.id == user.id:
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
    """
    指定された曲の各メダルの枚数を返す
    @param {int} music_id 曲ID
    @return {json} 各メダルの枚数, メダルの総数
    """
    if is_xml_http_request(request):
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
    """
    指定されたレベルのフォルダランプを返す
    @param {int} level レベル
    @param {bool} ?is_srandom S乱レベルかどうか
    @param {int} ?user_id ユーザーID
    @return {json} フォルダランプ
    """
    if is_xml_http_request(request):
        if request.user.is_authenticated:
            # ユーザーを取得
            try:
                # クエリでユーザーIDが指定されればそのユーザーを取得
                user_id = request.GET['user_id']
                user = get_object_or_404(CustomUser, pk=user_id)

                # 権限を確認
                if user != request.user:
                    if not user.is_active or user.cleardata_privacy == 2:
                        raise PermissionDenied
            except KeyError:
                user = request.user

            # 指定されたレベルの曲を取得
            level = int(level)
            if request.GET['is_srandom'] == 'true':
                max_lv = 19
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
                elif 5 <= medal.medal <= 7 and hard_flg:
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
                if 8 <= medal_max <= 10:
                    folder_lamp = 'failed'
                else:
                    folder_lamp = 'easy-cleared'

            # 全曲プレイ済みの場合
            elif medal_max:
                if medal_max == 1:
                    folder_lamp = 'perfect'
                elif 2 <= medal_max <= 4:
                    folder_lamp = 'fullcombo'
                elif 5 <= medal_max <= 7:
                    if hard_flg:
                        folder_lamp = 'hard-cleared'
                    else:
                        folder_lamp = 'cleared'
                elif 8 <= medal_max <= 10:
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


def is_xml_http_request(req: HttpRequest) -> bool:
    return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
