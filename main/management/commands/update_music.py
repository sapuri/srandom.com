import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from main.models import Difficulty, Level, Music, Sran_Level

from slack_sdk.webhook import WebhookClient


class Command(BaseCommand):
    help = 'CSVファイルから曲情報を読み取り、データベースを更新します。'

    logger = logging.getLogger('command.update_music')

    def __init__(self):
        super(Command, self).__init__()
        self.difficulties = {}
        self.levels = {}
        self.sran_levels = {}
        self.existing_musics = {}

    def handle(self, *args, **options):
        file_path = f'{settings.BASE_DIR}/csv/srandom.csv'

        music_list = self.parse_csv(file_path)

        self.difficulties = {difficulty.difficulty: difficulty for difficulty in Difficulty.objects.all()}
        self.levels = {level.level: level for level in Level.objects.all()}
        self.sran_levels = {sran_level.level: sran_level for sran_level in Sran_Level.objects.all()}
        self.existing_musics = {(music.title, music.difficulty.difficulty): music for music in
                                Music.objects.select_related('difficulty')}

        try:
            with transaction.atomic():
                update_msgs = self.update_db(music_list, Sran_Level.MAX)
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
        sran_level = max_lv
        update_msgs = []
        new_musics = []
        updated_musics = []

        for row in music_list:
            if len(row) == 1:
                sran_level -= 1
                continue

            level, title, bpm = int(row[0]), row[1], row[2]
            title, difficulty_key = self.split_difficulty(title)
            if difficulty_key not in self.difficulties:
                self.logger.warning(f'[skip] undefined difficulty: {title}')
                continue

            difficulty_obj = self.difficulties[difficulty_key]
            level_obj = self.levels.get(level)
            sran_level_obj = self.sran_levels.get(sran_level)

            if not level_obj or not sran_level_obj:
                self.logger.error(f'Level or Sran_Level not found: {level}, {sran_level}')
                continue

            music_key = (title, difficulty_key)

            if music_key in self.existing_musics:
                music = self.existing_musics[music_key]
                has_changed = False
                if music.level != level_obj or music.sran_level != sran_level_obj or music.bpm != bpm:
                    music.level = level_obj
                    music.sran_level = sran_level_obj
                    music.bpm = bpm
                    has_changed = True

                if has_changed:
                    updated_musics.append(music)
                    update_msgs.append(f'#{music.id}: {music.title}({music.difficulty}) を更新しました。')
            else:
                new_music = Music(
                    title=title,
                    difficulty=difficulty_obj,
                    level=level_obj,
                    sran_level=sran_level_obj,
                    bpm=bpm
                )
                new_musics.append(new_music)
                update_msgs.append(f'{new_music.title}({new_music.difficulty}) を追加しました。')

        if new_musics:
            Music.objects.bulk_create(new_musics)
        if updated_musics:
            Music.objects.bulk_update(updated_musics, ['level', 'sran_level', 'bpm'])

        return update_msgs

    def detect_deleted_songs(self, music_list: list) -> list:
        """
        データベースに存在するがCSVファイルには存在しない曲を検出
        :param music_list:
        :return: deleted_msgs
        """
        csv_titles_difficulties = {(self.split_difficulty(row[1])[0], self.split_difficulty(row[1])[1]) for row in
                                   music_list if len(row) > 1}
        deleted_musics = set(self.existing_musics.keys()) - csv_titles_difficulties

        deleted_msgs = []
        for title, difficulty in deleted_musics:
            music = self.existing_musics[(title, difficulty)]
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
