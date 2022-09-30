from django import template

register = template.Library()

# リストの添字に変数を与える


@register.filter
def get_at_index(list, index):
    return list[index]

# 2つの変数をコンマで区切った文字列を作成 (filterに3つ引数を渡すため)


@register.filter
def join_comma(var, args):
    return "%s,%s" % (var, args)

# 指定された曲の値をlistから探して返す


@register.filter
def medal_int(medal_list, music):
    if not medal_list:
        return 0

    for medal in medal_list:
        if medal.music.id == music.id:
            if medal.int() != 12:
                # 未プレイ以外ならメダルを返す
                return medal.int()   # 1-11
            else:
                return 0
    return 0


@register.filter
def bad_count_int(bad_count_list, music):
    if not bad_count_list:
        return '-'

    for bad_count in bad_count_list:
        if bad_count.music.id == music.id:
            return bad_count.int()
    return '-'


@register.filter
def bad_count_updated_at(bad_count_list, music):
    if not bad_count_list:
        return '-'

    for bad_count in bad_count_list:
        if bad_count.music.id == music.id:
            return bad_count.updated_at
    return '-'


@register.filter
def is_hard(extra_option_list, music):
    if not extra_option_list:
        return False

    for extra_option in extra_option_list:
        if extra_option.music.id == music.id:
            if extra_option.is_hard():
                return True
            else:
                return False
