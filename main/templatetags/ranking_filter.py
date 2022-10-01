from django import template

register = template.Library()

# 指定された曲の平均BAD数を返す


@register.filter
def bad_count_avg(bad_count_list, music):
    if not bad_count_list:
        return None

    bad_count_sum = 0   # BAD数の合計
    bad_count_num = 0   # BAD数の個数

    for bad_count in bad_count_list:
        if bad_count.music.id == music.id:
            bad_count_sum += bad_count.int()
            bad_count_num += 1

    # BAD数の平均を計算 (小数点以下四捨五入)
    bad_count_avg = round(bad_count_sum / bad_count_num)

    return bad_count_avg

# 指定された曲の順位を返す


@register.filter
def bad_count_rank(bad_count_list_ordered, music_id_and_myself_id):
    '''
    指定された曲の順位を返す
    @param bad_count_list_ordered: 昇順で整列済のBAD数リスト
    @param music_id_and_myself_id: 曲IDと自ユーザーIDをコンマで区切った文字列
    '''
    if not bad_count_list_ordered:
        return '-'

    # コンマで分割
    music_id_and_myself_id = music_id_and_myself_id.split(",")
    music_id = int(music_id_and_myself_id[0])
    myself_id = int(music_id_and_myself_id[1])

    bad_count_num = 0   # BAD数の個数
    bad_count_now = -1  # 現在のBAD数
    myrank = -1         # 自ランク
    found = False       # BAD数を登録済であればTrueを返す

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
        return '- / %d' % (bad_count_num)
    else:
        return '- / -'
