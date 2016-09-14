from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import csv

from users.models import CustomUser
from main.models import Bad_Count, Medal, Extra_Option, Music

class Command(BaseCommand):
    help = 'プレミアムユーザーのクリアデータを CSV にエクスポートします。'

    def handle(self, *args, **options):
        # FIXME: メダルが存在しない記録を読み込むとエラーになる

        username = ''

        if username:
            print ('ユーザー名が指定されました\n')
            selected_users = CustomUser.objects.filter(username=username)
        else:
            # プレミアムユーザーを取得
            selected_users = CustomUser.objects.filter(is_active=True, premium=True)
            selected_users_count = CustomUser.objects.filter(is_active=True, premium=True).count()
            print ('active premium user: '+str(selected_users.count())+' users\n')

        for selected_user in selected_users:
            print ('"{username}" のクリアデータを読み込んでいます...'.format(username=selected_user.username))

            # CSV書き込み用データ (2次元配列)
            csv_data = [['S乱Lv', 'Lv', '曲名', '難易度', 'BPM', 'メダル', 'ハード', 'BAD数', '更新日時']]

            max_s_lv = 17
            s_lv_range = range(max_s_lv, 0, -1)
            for s_lv in s_lv_range:
                sran_level_id = max_s_lv - s_lv + 1
                music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')
                for music in music_list:
                    try:
                        bad_count = Bad_Count.objects.get(music=music, user=selected_user)
                    except ObjectDoesNotExist:
                        bad_count = ''
                    try:
                        medal = Medal.objects.get(music=music, user=selected_user)
                    except ObjectDoesNotExist:
                        medal = ''
                    try:
                        extra_option = Extra_Option.objects.get(music=music, user=selected_user)
                        if extra_option.hard:
                            hard = '○'
                        else:
                            hard = ''
                    except ObjectDoesNotExist:
                        hard = ''
                    updated_at = get_latest_updated_at(music.id, selected_user.id)

                    row = [music.sran_level, music.level, music.title, music.difficulty, music.bpm, medal, hard, bad_count, updated_at]
                    # print (row) # debug
                    csv_data.append(row)
                if s_lv != 1:
                    csv_data.append(['', '', '', '', '', '', '', '', ''])

            # CSVファイルに書き込み
            BASE_DIR = '/Users/minami/workspace/srandom.com'   # ローカル
            # BASE_DIR = '/var/www/srandom.com'                  # VPS
            file_path = BASE_DIR+'/csv/export/'+selected_user.username+'.csv'
            f = open(file_path, 'w')
            writer = csv.writer(f)
            writer.writerows(csv_data)
            f.close()

            print ('"{username}" のクリアデータを出力しました: {username}.csv\n'.format(username=selected_user.username))

        print ('Complete!')

def get_latest_updated_at(music_id, user_id):
    '''
    @param {int} music_id 曲ID
    @param {int} user_id ユーザーID
    @return {string} 最新の更新日時
    '''
    try:
        bad_count = Bad_Count.objects.get(music=music_id, user=user_id)
    except ObjectDoesNotExist:
        bad_count = None
    try:
        medal = Medal.objects.get(music=music_id, user=user_id)
    except ObjectDoesNotExist:
        medal = None
    try:
        extra_option = Extra_Option.objects.get(music=music_id, user=user_id)
    except ObjectDoesNotExist:
        extra_option = None

    # 最新の更新日時を取得
    if bad_count and medal and extra_option:
        bad_count_updated_at = bad_count.updated_at
        medal_updated_at = medal.updated_at
        extra_option_updated_at = extra_option.updated_at
        latest = max(bad_count_updated_at, medal_updated_at, extra_option_updated_at)
    elif bad_count and medal:
        bad_count_updated_at = bad_count.updated_at
        medal_updated_at = medal.updated_at
        extra_option_updated_at = None
        latest = max(bad_count_updated_at, medal_updated_at)
    elif medal and extra_option:
        bad_count_updated_at = None
        medal_updated_at = medal.updated_at
        extra_option_updated_at = extra_option.updated_at
        latest = max(medal_updated_at, extra_option_updated_at)
    elif bad_count:
        bad_count_updated_at = bad_count.updated_at
        medal_updated_at = None
        extra_option_updated_at = None
        latest = bad_count_updated_at
    elif medal:
        bad_count_updated_at = None
        medal_updated_at = medal.updated_at
        extra_option_updated_at = None
        latest = medal_updated_at
    elif extra_option:
        bad_count_updated_at = None
        medal_updated_at = None
        extra_option_updated_at = extra_option.updated_at
        latest = extra_option_updated_at
    else:
        bad_count_updated_at = None
        medal_updated_at = None
        extra_option_updated_at = None
        latest = None

    if latest:
        # 時間調整
        latest_hour = latest.hour + 9   # UTC+9
        latest_day = latest.day
        if latest_hour > 24:
            latest_day += 1
            latest_hour -= 24
        return ("%d/%d/%02d %d:%02d") % (latest.year, latest.month, latest_day, latest_hour, latest.minute)
    else:
        return ''
