from django import template

register = template.Library()

@register.filter
def count_medal(medal_list, medal_int):
    '''
    指定された種類のメダルを数える
    @param list|medal_list: 曲で絞込済みのメダルリスト
    @param int|medal_int: 指定されたメダル
    @return int|medal_num: 指定されたメダルの枚数
    '''
    if not medal_list and (medal_int < 1 or medal_int > 11):
        return 0

    medal_num = 0

    for medal in medal_list:
        if medal.int() == medal_int:
            # メダルをカウント
            medal_num += 1

    return medal_num

@register.filter
def count_medal_total(medal_list):
    '''
    未クリア以外の全てのメダルを数える
    @param list|medal_list: 曲で絞込済みのメダルリスト
    @return int|medal_num: 指定されたメダルの枚数
    '''
    if not medal_list:
        return 0

    medal_num = 0

    for medal in medal_list:
        if medal.int() != 12:
            # メダルをカウント
            medal_num += 1

    return medal_num

'''
指定された曲の平均BAD数を返す
@param list|bad_count_list: 曲で絞り込み済のBAD数リスト
@param CustomUser|user: 指定されたユーザー
@return int|bad_count_avg: 平均BAD数
'''
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

@register.filter
def bad_count_rank(bad_count_list_ordered, user):
    '''
    曲とユーザーを指定で順位を返す
    @param list|bad_count_list_ordered: 曲で絞込済みのBAD数リスト(昇順)
    @param CustomUser|user: 指定されたユーザー
    @return int|rank: 順位
    '''
    if not bad_count_list_ordered:
        return None

    bad_count_num = 0   # BAD数の個数
    bad_count_now = -1  # 現在のBAD数
    rank = -1           # ランク
    found = False       # BAD数を登録済であればTrueを返す

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

@register.filter
def medal_int(medal_list, user):
    '''
    指定されたユーザーのメダルをlistから探して返す
    @param list|medal_list: 曲で絞込済みのメダルリスト
    @param CustomUser|user: 指定されたユーザー
    @return int|0〜12: メダル
    '''
    if not medal_list:
        return 0

    for medal in medal_list:
        if medal.user.id == user.id:
            if medal.int() != 12:
                # 未プレイ以外ならメダルを返す
                return medal.int()   # 1-11
            else:
                return 0

    return 0

@register.filter
def bad_count_int(bad_count_list, user):
    '''
    指定されたユーザーのBAD数をlistから探して返す
    @param list|bad_count_list: 曲で絞込済みのBAD数リスト
    @param CustomUser|user: 指定されたユーザー
    @return int: BAD数
    '''
    if not bad_count_list:
        return None

    for bad_count in bad_count_list:
        if bad_count.user.id == user.id:
            return bad_count.int()

    return None

@register.filter
def bad_count_updated_at(bad_count_list, user):
    '''
    指定されたユーザーのBAD数をlistから探して返す
    @param list|bad_count_list: 曲で絞込済みのBAD数リスト
    @param CustomUser|user: 指定されたユーザー
    @return datetime|bad_count_updated_at: 更新日時
    '''
    if not bad_count_list:
        return None

    for bad_count in bad_count_list:
        if bad_count.user.id == user.id:
            return bad_count.updated_at
    return None

@register.filter
def is_hard(extra_option_list, user):
    if not extra_option_list:
        return False

    for extra_option in extra_option_list:
        if extra_option.user.id == user.id:
            if extra_option.is_hard():
                return True
            else:
                return False
