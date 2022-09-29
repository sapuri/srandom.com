import concurrent.futures
import csv
import logging
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from google.cloud import storage
from google.cloud.storage import Bucket

from main.models import Bad_Count, Medal, Extra_Option, Music
from users.models import CustomUser


class Command(BaseCommand):
    help = 'プレミアムユーザーのクリアデータを CSV にエクスポートします。'

    logger = logging.getLogger('command.export2csv')

    def handle(self, *args, **options):
        # FIXME: メダルが存在しない記録を読み込むとエラーになる

        env = getattr(settings, 'ENV', None)
        if env is None:
            raise Exception('failed to read env')

        storage_client = storage.Client()
        bucket = storage_client.bucket(env('GCP_INTERNAL_BUCKET'))

        os.makedirs(f'{settings.BASE_DIR}/csv/export/', exist_ok=True)

        username = ''

        if username:
            self.logger.info('ユーザー名が指定されました')
            selected_users = CustomUser.objects.filter(username=username)
        else:
            # プレミアムユーザーを取得
            selected_users = CustomUser.objects.filter(is_active=True, premium=True)
            self.logger.info(f'active premium user: {selected_users.count()} users')

        futures = []
        for selected_user in selected_users:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures.append(executor.submit(self.invoke, selected_user, bucket))

        for f in concurrent.futures.as_completed(futures):
            f.result()

        self.logger.info('Finished')

    def invoke(self, user: CustomUser, bucket: Bucket):
        self.logger.info(f'{user.username}" のクリアデータを読み込んでいます...')

        # CSV書き込み用データ (2次元配列)
        csv_data = [['S乱Lv', 'Lv', '曲名', '難易度', 'BPM', 'メダル', 'ハード', 'BAD数', '更新日時']]

        max_s_lv = 19
        s_lv_range = range(max_s_lv, 0, -1)
        for s_lv in s_lv_range:
            sran_level_id = s_lv
            music_list = Music.objects.filter(sran_level=sran_level_id).order_by('level', 'title')
            for music in music_list:
                try:
                    bad_count = Bad_Count.objects.get(music=music, user=user)
                except ObjectDoesNotExist:
                    bad_count = ''
                try:
                    medal = Medal.objects.get(music=music, user=user)
                except ObjectDoesNotExist:
                    medal = ''
                try:
                    extra_option = Extra_Option.objects.get(music=music, user=user)
                    if extra_option.hard:
                        hard = '○'
                    else:
                        hard = ''
                except ObjectDoesNotExist:
                    hard = ''
                updated_at = self.get_latest_updated_at(music.id, user.id)

                row = [music.sran_level, music.level, music.title, music.difficulty, music.bpm, medal, hard, bad_count, updated_at]
                csv_data.append(row)
            if s_lv != 1:
                csv_data.append(['', '', '', '', '', '', '', '', ''])

        # CSVファイルに書き込み
        file_path = f'{settings.BASE_DIR}/csv/export/{user.username}.csv'
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        blob = bucket.blob(f'csv/export/{user.username}.csv')
        blob.upload_from_filename(file_path)

        self.logger.info(f'"{user.username}" のクリアデータを出力しました: {user.username}.csv')

    @staticmethod
    def get_latest_updated_at(music_id: int, user_id: int) -> str:
        """
        :param music_id: 曲ID
        :param user_id: ユーザーID
        :return: 最新の更新日時
        """
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
            latest = max(bad_count.updated_at, medal.updated_at, extra_option.updated_at)
        elif bad_count and medal:
            latest = max(bad_count.updated_at, medal.updated_at)
        elif medal and extra_option:
            latest = max(medal.updated_at, extra_option.updated_at)
        elif bad_count:
            latest = bad_count.updated_at
        elif medal:
            latest = medal.updated_at
        elif extra_option:
            latest = extra_option.updated_at
        else:
            latest = None

        if latest:
            # 時間調整
            latest_hour = latest.hour + 9  # UTC+9
            latest_day = latest.day
            if latest_hour > 24:
                latest_day += 1
                latest_hour -= 24
            return "%d/%d/%02d %d:%02d" % (latest.year, latest.month, latest_day, latest_hour, latest.minute)

        return ''
