from django.db.models import QuerySet

from main.models import Extra_Option, Medal

from users.models import CustomUser


def get_folder_status(user: CustomUser, music_query: QuerySet) -> Medal.ClearStatus:
    medals = Medal.objects.filter(music__in=music_query, user=user)
    extra_options = Extra_Option.objects.filter(music__in=music_query, user=user, hard=True).values_list('music_id',
                                                                                                         flat=True)

    medal_max = 0
    easy_flg = False
    hard_flg = True

    for music in music_query:
        medal = medals.filter(music_id=music.id).first()
        if not medal or medal.medal == 12:
            return Medal.ClearStatus.NO_PLAY
        if medal.medal == 11:
            easy_flg = True
        if 5 <= medal.medal <= 7 and music.id not in extra_options:
            hard_flg = False
        medal_max = max(medal_max, medal.medal if medal else 0)

    if easy_flg and medal_max < 8:
        return Medal.ClearStatus.EASY_CLEARED
    elif easy_flg:
        return Medal.ClearStatus.FAILED
    elif medal_max == 1:
        return Medal.ClearStatus.PERFECT
    elif 2 <= medal_max <= 4:
        return Medal.ClearStatus.FULL_COMBO
    elif 5 <= medal_max <= 7:
        return Medal.ClearStatus.HARD_CLEARED if hard_flg else Medal.ClearStatus.CLEARED
    elif 8 <= medal_max <= 10:
        return Medal.ClearStatus.FAILED
    else:
        return Medal.ClearStatus.NO_PLAY
