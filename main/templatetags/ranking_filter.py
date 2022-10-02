from django import template

from main.models import Music, Bad_Count

register = template.Library()


@register.filter
def bad_count_avg(bad_count_list: list[Bad_Count], music: Music) -> int | None:
    """
    指定された曲の平均BAD数を返す
    :param bad_count_list:
    :param music:
    :return: 平均BAD数
    """
    if not bad_count_list:
        return None

    bad_count_sum = 0  # BAD数の合計
    bad_count_num = 0  # BAD数の個数

    for bad_count in bad_count_list:
        if bad_count.music.id == music.id:
            bad_count_sum += bad_count.int()
            bad_count_num += 1

    # BAD数の平均を計算 (小数点以下四捨五入)
    return round(bad_count_sum / bad_count_num)


@register.filter
def bad_count_rank(bad_count_list_ordered: list[Bad_Count], music_id_and_myself_id: str) -> str:
    """
    指定された曲の順位を返す
    :param bad_count_list_ordered:
    :param music_id_and_myself_id:
    :return: 順位
    """
    if not bad_count_list_ordered:
        return '-'

    # コンマで分割
    music_id_and_myself_id = music_id_and_myself_id.split(",")
    music_id = int(music_id_and_myself_id[0])
    myself_id = int(music_id_and_myself_id[1])

    bad_count_num = 0  # BAD数の個数
    bad_count_now = -1  # 現在のBAD数
    myrank = -1  # 自ランク
    found = False  # BAD数を登録済であればTrueを返す
    tmp_rank = 0

    for bad_count in bad_count_list_ordered:
        if bad_count.music.id == music_id:
            bad_count_before = bad_count_now
            bad_count_now = bad_count.bad_count

            # BAD数が前後で重複した場合
            if bad_count_now == bad_count_before:
                # 指定されたユーザーの記録が見つかれば myrank にランクを格納
                if bad_count.user.id == myself_id:
                    found = True
                    myrank = tmp_rank

                bad_count_num += 1

            # BAD数が重複しなかった場合
            else:
                bad_count_num += 1

                # 一時ランクを更新
                tmp_rank = bad_count_num

                # 自分の記録が見つかれば myrank にランクを格納
                if bad_count.user.id == myself_id:
                    found = True
                    myrank = bad_count_num

    if found:
        return '%d / %d' % (myrank, bad_count_num)
    elif bad_count_num != 0:
        return '- / %d' % bad_count_num
    else:
        return '- / -'
