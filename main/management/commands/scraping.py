import csv
import logging
import os

from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import BaseCommand

import requests


class Command(BaseCommand):
    help = 'S乱難易度表から曲情報を取得し、CSVファイルに出力します。'

    logger = logging.getLogger('command.scraping')

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            default=False,
            help='エラー以外の表示をオフにします。 (default: False)'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        # S乱クリア難易度表1 (Lv11-19)
        url1 = 'https://popn.wiki/%E3%81%9D%E3%81%AE%E4%BB%96/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93' \
               '%E5%BA%A6%E8%A1%A8/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A81'
        # S乱クリア難易度表2 (Lv5-10)
        url2 = 'https://popn.wiki/%E3%81%9D%E3%81%AE%E4%BB%96/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93' \
               '%E5%BA%A6%E8%A1%A8/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A82'
        # S乱クリア難易度表3 (Lv2弱-4)
        url3 = 'https://popn.wiki/%E3%81%9D%E3%81%AE%E4%BB%96/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93' \
               '%E5%BA%A6%E8%A1%A8/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A83'
        # S乱クリア難易度表4 (Lv1弱-1強)
        url4 = 'https://popn.wiki/%E3%81%9D%E3%81%AE%E4%BB%96/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93' \
               '%E5%BA%A6%E8%A1%A8/s%E4%B9%B1%E3%82%AF%E3%83%AA%E3%82%A2%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A84'

        file_path = f'{settings.BASE_DIR}/csv/srandom.csv'
        os.makedirs(f'{settings.BASE_DIR}/csv/', exist_ok=True)

        csv_data = self.scrape(url1, mode=1, silent=silent)
        self.generate_csv(csv_data, file_path, append=False)

        csv_data = self.scrape(url2, mode=2, silent=silent)
        self.generate_csv(csv_data, file_path, append=True)

        csv_data = self.scrape(url3, mode=3, silent=silent)
        self.generate_csv(csv_data, file_path, append=True)

        csv_data = self.scrape(url4, mode=4, silent=silent)
        self.generate_csv(csv_data, file_path, append=True)

    def scrape(self, url: str, mode: int, silent: bool = False) -> list:
        """
        難易度表から曲情報を取得
        :param url:
        :param mode: 1=Lv5〜Lv19, 2=Lv4〜Lv1
        :param mode: 1=Lv11〜Lv19, 2=Lv5〜Lv10, 3=Lv2弱〜4, 4=Lv1弱〜Lv1強
        :param silent: True=エラー以外の表示をオフ
        :return: csv data
        """
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'lxml')

        csv_data = []

        level_range = []
        if mode == 1:
            # Lv19〜Lv11を取得
            level_range = range(19, 10, -1)
        elif mode == 2:
            # Lv10〜Lv5を取得
            level_range = range(10, 4, -1)
        elif mode == 3:
            # Lv2弱〜Lv4を取得
            level_range = ['4', '3', '2強', '2弱']
        elif mode == 4:
            # Lv1弱〜Lv1強を取得
            level_range = ['1強', '1弱']
        else:
            self.logger.error(f'invalid mode: {mode}')
            quit(1)

        for i, j in enumerate(level_range):
            # Lv表記を取得
            h2 = soup.select(f'h2#lv{j}')[0]
            level = h2.text[1:].strip()
            if not silent:
                self.logger.info(level)

            if j == '2強' or j == '2弱':
                level = 'Lv2'
            elif j == '1強' or j == '1弱':
                level = 'Lv1'

            if j == '2弱' or j == '1弱':
                music_list = []
            else:
                music_list = [[level]]

            # table の tr を走査
            table = h2.next_sibling.next_sibling.table.children
            for i, tr in enumerate(table):
                if i < 4 or tr == '\n':
                    continue

                td_list = tr.find_all('td')
                lv = td_list[0].text.strip()
                title = td_list[1].a.text.strip()
                bpm = td_list[2].text.strip()
                music_list.append([lv, title, bpm])

                if not silent:
                    self.logger.info(title)

            csv_data.append([music_list])

        return csv_data

    @staticmethod
    def generate_csv(csv_data: list, file_path: str, append: bool = False):
        """
        CSV を生成
        :param csv_data:
        :param file_path:
        :param append:
        """
        mode = 'w'
        if append:
            mode = 'a'

        with open(file_path, mode) as f:
            writer = csv.writer(f, lineterminator='\n')

            if not append:
                column_mame = ['レベル', '曲名', 'BPM']
                writer.writerow(column_mame)

            for lines in csv_data:
                for line in lines:
                    writer.writerows(line)
