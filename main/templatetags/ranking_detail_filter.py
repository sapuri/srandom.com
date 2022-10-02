from django import template

from main.models import Bad_Count, Medal, Extra_Option
from users.models import CustomUser

register = template.Library()


@register.filter
def bad_count_rank(bad_count_list_ordered: list[Bad_Count], user: CustomUser) -> int | None:
    """
    曲とユーザーを指定で順位を返す
    :param bad_count_list_ordered: 曲で絞込済みのBAD数リスト(昇順)
    :param user: 指定されたユーザー
    :return: 順位
    """
    if not bad_count_list_ordered:
        return None

    bad_count_num = 0   # BAD数の個数
    bad_count_now = -1  # 現在のBAD数
    rank = -1           # ランク
    found = False       # BAD数を登録済であればTrueを返す
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


@register.filter
def medal_int(medal_list: list[Medal], user: CustomUser) -> int:
    """
    指定されたユーザーのメダルをlistから探して返す
    :param medal_list: 曲で絞込済みのメダルリスト
    :param user: 指定されたユーザー
    :return: メダル (0-12)
    """
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
def bad_count_int(bad_count_list: list[Bad_Count], user: CustomUser) -> int | None:
    """
    指定されたユーザーのBAD数をlistから探して返す
    :param bad_count_list: 曲で絞込済みのBAD数リスト
    :param user: 指定されたユーザー
    :return: BAD数
    """
    if not bad_count_list:
        return None

    for bad_count in bad_count_list:
        if bad_count.user.id == user.id:
            return bad_count.int()

    return None


@register.filter
def bad_count_updated_at(bad_count_list: list[Bad_Count], user: CustomUser):
    """
    指定されたユーザーのBAD数をlistから探して返す
    :param bad_count_list: 曲で絞込済みのBAD数リスト
    :param user: 指定されたユーザー
    :return: 更新日時 (datetime)
    """
    if not bad_count_list:
        return None

    for bad_count in bad_count_list:
        if bad_count.user.id == user.id:
            return bad_count.updated_at

    return None


@register.filter
def is_hard(extra_option_list: list[Extra_Option], user: CustomUser) -> bool:
    if not extra_option_list:
        return False

    for extra_option in extra_option_list:
        if extra_option.user.id == user.id:
            if extra_option.is_hard():
                return True
            else:
                return False
