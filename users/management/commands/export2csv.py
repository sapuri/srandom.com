import concurrent.futures
import csv
import logging
import os
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

from google.cloud import storage
from google.cloud.storage import Bucket

from main.models import Bad_Count, Extra_Option, Medal, Music

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

        futures = []
        for selected_user in CustomUser.objects.filter(is_active=True, premium=True):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures.append(executor.submit(self.invoke, selected_user, bucket))

        for f in concurrent.futures.as_completed(futures):
            f.result()

        self.logger.info('Finished')

    def invoke(self, user: CustomUser, bucket: Bucket):
        self.logger.info(f'{user.username}" のクリアデータを読み込んでいます...')

        bad_counts = {(bc.music_id, bc.user_id): bc for bc in Bad_Count.objects.filter(user=user)}
        medals = {(m.music_id, m.user_id): m for m in Medal.objects.filter(user=user)}
        extra_options = {(eo.music_id, eo.user_id): eo for eo in Extra_Option.objects.filter(user=user)}

        csv_data = self.generate_csv_data(user, bad_counts, medals, extra_options)

        self.write_to_csv_and_upload(user.username, csv_data, bucket)
        self.logger.info(f'"{user.username}" のクリアデータを出力しました: {user.username}.csv')

        connections.close_all()

    def generate_csv_data(self, user: CustomUser, bad_counts: dict, medals: dict, extra_options: dict) -> list:
        csv_data = [['S乱Lv', 'Lv', '曲名', '難易度', 'BPM', 'メダル', 'ハード', 'BAD数', '更新日時']]

        for s_lv in range(19, 0, -1):
            music_list = Music.objects.filter(sran_level=s_lv).order_by('level', 'title')
            for music in music_list:
                key = (music.id, user.id)
                bad_count = bad_counts.get(key)
                medal = medals.get(key)
                extra_option = extra_options.get(key)

                row = [
                    s_lv,
                    music.level,
                    music.title,
                    music.difficulty,
                    music.bpm,
                    medal if medal else '',
                    '○' if extra_option and extra_option.hard else '',
                    bad_count if bad_count else '',
                    self.get_latest_updated_at(bad_count, medal, extra_option)
                ]
                csv_data.append(row)

        return csv_data

    @staticmethod
    def write_to_csv_and_upload(username: str, csv_data: list, bucket: Bucket):
        file_path = f'{settings.BASE_DIR}/csv/export/{username}.csv'
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        blob = bucket.blob(f'csv/export/{username}.csv')
        blob.upload_from_filename(file_path)

    @staticmethod
    def get_latest_updated_at(bad_count: Bad_Count, medal: Medal, extra_option: Extra_Option) -> str:
        dates = []

        if bad_count is not None:
            dates.append(bad_count.updated_at)

        if medal is not None:
            dates.append(medal.updated_at)

        if extra_option is not None:
            dates.append(extra_option.updated_at)

        if dates:
            latest_date_jst = max(dates).astimezone(ZoneInfo('Asia/Tokyo'))
            return latest_date_jst.strftime('%Y/%m/%d %H:%M')

        return ''
