from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models import Music, Medal, Bad_Count, Extra_Option
from users.models import CustomUser


def ranking_detail(request: HttpRequest, music_id: int) -> HttpResponse:
    """ ランキング: 詳細 """

    def bad_count_rank(bad_count_list_ordered: list[Bad_Count], user: CustomUser) -> int | None:
        """
        指定されたユーザーの順位を返す
        @param bad_count_list_ordered: 曲で絞込済みのBAD数リスト(昇順)
        @param user: 指定されたユーザー
        @return rank: 順位
        """
        if not bad_count_list_ordered:
            return None

        bad_count_num = 0  # BAD数の個数
        bad_count_now = -1  # 現在のBAD数
        rank = -1  # ランク
        found = False  # BAD数を登録済であればTrueを返す
        tmp_rank = 0

        for bad_count in bad_count_list_ordered:
            bad_count_before = bad_count_now
            bad_count_now = bad_count.bad_count

            # BAD数が前後で重複した場合
            if bad_count_now == bad_count_before:
                # 指定されたユーザーの記録が見つかれば rank にランクを格納
                if bad_count.user.id == user.id:
                    found = True
                    rank = tmp_rank

                bad_count_num += 1

            # BAD数が重複しなかった場合
            else:
                bad_count_num += 1

                # 一時ランクを更新
                tmp_rank = bad_count_num

                # 自分の記録が見つかれば rank にランクを格納
                if bad_count.user.id == user.id:
                    found = True
                    rank = bad_count_num

        if found:
            return rank
        else:
            return None

    # 曲を取得
    music = get_object_or_404(Music, pk=music_id)

    medal_list = Medal.objects.filter(music=music)
    bad_count_list = Bad_Count.objects.filter(music=music).order_by('bad_count', 'updated_at')
    extra_option_list = Extra_Option.objects.filter(music=music)

    # 対象曲を記録しているユーザーを取得
    user_id_list = list(bad_count_list.values_list('user', flat=True))
    users = CustomUser.objects.filter(pk__in=user_id_list, is_active=True)

    # ランキングを生成
    results = []
    for bad_count in bad_count_list:
        selected_user = users.get(pk=bad_count.user.id)
        try:
            medal = medal_list.get(user=selected_user)
            if medal.medal == 12:
                medal = None
        except ObjectDoesNotExist:
            medal = None
        try:
            extra_option = extra_option_list.get(user=selected_user)
        except ObjectDoesNotExist:
            extra_option = None
        rank = bad_count_rank(bad_count_list, selected_user)
        results.append({
            'rank': rank,
            'user': selected_user,
            'medal': medal,
            'bad_count': bad_count,
            'extra_option': extra_option
        })

    context = {
        'music': music,
        'bad_count_list': bad_count_list,
        'results': results
    }

    return render(request, 'main/ranking_detail.html', context)
