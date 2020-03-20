import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError

from main.models import Music, Difficulty, Level, Sran_Level


class Command(BaseCommand):
    help = 'CSVファイルから曲情報を読み取り、データベースを更新します。'

    def handle(self, *args, **options):
        file_path = f'{settings.BASE_DIR}/csv/srandom.csv'
        max_lv = 19

        music_list = self.parse_csv(file_path)
        update_count = self.update_db(music_list, max_lv)
        if update_count:
            print(f'更新が {update_count}件 ありました！')

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

    def update_db(self, music_list: list, max_lv: int) -> int:
        """
        :param music_list:
        :param max_lv:
        :return: update_count
        """
        sran_level = max_lv
        update_count = 0

        for row in music_list:
            if len(row) == 1:
                sran_level -= 1
                continue

            level = int(row[0])
            title = row[1]
            bpm = row[2]

            title, difficulty = self.split_difficulty(title)
            if not difficulty:
                print('[skip] undefined difficulty:', title)
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
                print(f'failed Music.objects.get_or_create with DataError: {music}\n')
                raise DataError

            if created:
                print(f'#{music.id}: {music.title}({music.difficulty}) を追加しました。')
                update_count += 1
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
                print(
                    f'#{music.id}: {music.title}({music.difficulty}) を S乱レベルID: {music.sran_level} レベル: {music.level} BPM: {music.bpm} に更新しました。')
                update_count += 1

        return update_count

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
            print('difficulty not found')
            return title, ''
