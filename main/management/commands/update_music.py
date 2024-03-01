import csv
import logging
import os

from slack_sdk.webhook import WebhookClient

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError, transaction

from main.models import Music, Difficulty, Level, Sran_Level


class Command(BaseCommand):
    help = 'CSVファイルから曲情報を読み取り、データベースを更新します。'

    logger = logging.getLogger('command.update_music')

    def handle(self, *args, **options):
        file_path = f'{settings.BASE_DIR}/csv/srandom.csv'
        max_lv = 19

        try:
            music_list = self.parse_csv(file_path)

            with transaction.atomic():
                update_msgs = self.update_db(music_list, max_lv)
                deleted_msgs = self.detect_deleted_songs(music_list)

            if update_msgs:
                self.notify_slack(f'更新が{len(update_msgs)}件ありました！\n```' + '\n'.join(update_msgs) + '```')
            if deleted_msgs:
                self.notify_slack(f'{len(deleted_msgs)}件の削除曲を検出しました\n```' + '\n'.join(deleted_msgs) + '```')
        except Exception as e:
            self.logger.error(f'an error occurred: {e}')
            quit(1)

        self.logger.info("finished updating music records.")

    @staticmethod
    def parse_csv(file_path: str) -> list:
        """
        :param file_path:
        :return: music_list
        """
        music_list = []

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            next(reader)

            for row in reader:
                music_list.append(row)

        return music_list

    def update_db(self, music_list: list, max_lv: int) -> list:
        """
        :param music_list:
        :param max_lv:
        :return: update_msgs
        """
        sran_level = max_lv
        update_msgs = []

        for row in music_list:
            if len(row) == 1:
                sran_level -= 1
                continue

            level = int(row[0])
            title = row[1]
            bpm = row[2]

            title, difficulty = self.split_difficulty(title)
            if not difficulty:
                self.logger.warning(f'[skip] undefined difficulty: {title}')
                continue

            try:
                music, created = Music.objects.get_or_create(
                    title=title,
                    difficulty=Difficulty.objects.get(difficulty=difficulty),
                    defaults={
                        'title': title,
                        'difficulty': Difficulty.objects.get(difficulty=difficulty),
                        'level': Level.objects.get(level=level),
                        'sran_level': Sran_Level.objects.get(level=sran_level),
                        'bpm': bpm
                    }
                )
            except DataError:
                self.logger.error(f'Music.objects.get_or_create failed with DataError: {music}')
                raise DataError

            if created:
                update_msgs.append(f'#{music.id}: {music.title}({music.difficulty}) を追加しました。')
                continue

            has_changed = False
            if music.level.level != level:
                music.level = Level.objects.get(level=level)
                has_changed = True
            if music.sran_level.level != sran_level:
                music.sran_level = Sran_Level.objects.get(level=sran_level)
                has_changed = True
            if music.bpm != bpm:
                music.bpm = bpm
                has_changed = True

            if has_changed:
                music.save(update_fields=['level', 'sran_level', 'bpm'])
                update_msgs.append(
                    f'#{music.id}: {music.title}({music.difficulty}) を S乱レベルID: {music.sran_level} レベル: {music.level} BPM: {music.bpm} に更新しました。')

        return update_msgs

    def detect_deleted_songs(self, music_list: list) -> list:
        """
        データベースに存在するがCSVファイルには存在しない曲を検出
        :param music_list:
        :return: deleted_msgs
        """
        csv_titles = {self.split_difficulty(row[1])[0] for row in music_list if len(row) > 1}
        db_titles = set(Music.objects.values_list('title', flat=True))

        deleted_from_csv = db_titles - csv_titles
        if not deleted_from_csv:
            return []

        deleted_msgs = []
        for title in deleted_from_csv:
            music = Music.objects.get(title=title)
            deleted_msgs.append(f'#{music.id}: {music.title}({music.difficulty})')

        return deleted_msgs

    def notify_slack(self, text: str):
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if not webhook_url:
            self.logger.error("SLACK_WEBHOOK_URL is not set")
            return

        resp = WebhookClient(webhook_url).send(text=text)
        if resp.status_code != 200:
            self.logger.error("failed to notify Slack: " + resp.body)

    @staticmethod
    def split_difficulty(title: str) -> tuple:
        """
        タイトルと難易度を分割
        :param title:
        :return: (title, difficulty)
        """
        spl = title[-4:]
        if '(EX)' in spl:
            return title[:-4], 'EXTRA'
        elif '(H)' in spl:
            return title[:-3], 'HYPER'
        elif '(N)' in spl:
            return title[:-3], 'NORMAL'
        elif '(E)' in spl:
            return title[:-3], 'EASY'
        else:
            return title, ''
