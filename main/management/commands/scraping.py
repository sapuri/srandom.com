import csv

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'S乱難易度表を取得して CSV を生成します。'

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            default=False,
            help='エラー以外の表示をオフにします。 (default: False)'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        url1 = 'https://hellwork.jp/popn/wiki/734.html'  # S乱クリア難易度表
        url2 = 'https://hellwork.jp/popn/wiki/?%E3%81%9D%E3%81%AE%E4%BB%96/S%E4%B9%B1Lv0%E9%9B%A3%E6%98%93%E5%BA%A6' \
               '%E8%A1%A8'  # S乱Lv0難易度表
        file_path = f'{settings.BASE_DIR}/csv/srandom.csv'

        csv_data = self.scrape(url1, mode=1, silent=silent)
        self.generate_csv(csv_data, file_path, append=False)

        csv_data = self.scrape(url2, mode=2, silent=silent)
        self.generate_csv(csv_data, file_path, append=True)

    @staticmethod
    def scrape(url: str, mode: int, silent: bool = False) -> list:
        """
        難易度表から曲情報を取得
        :param url:
        :param mode: 1=Lv5〜Lv19, 2=Lv4〜Lv1
        :param silent: True=エラー以外の表示をオフ
        :return: csv data
        """
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'lxml')

        csv_data = []

        level_range = []
        if mode == 1:
            # Lv5〜Lv19を取得
            # #content_1_2 〜 #content_1_16 を指定
            level_range = range(2, 17)
        elif mode == 2:
            # Lv4〜Lv1を取得
            # #content_1_1 〜 #content_1_6 を指定
            level_range = range(1, 7)
        else:
            print(f'invalid mode: {mode}')
            quit(1)

        for i, j in enumerate(level_range):
            # Lv表記を取得
            h3 = soup.select(f'h3#content_1_{j}')[0].text[1:-1].strip()
            if not silent:
                print(h3)

            if mode == 2:
                if j == 3:  # Lv2強
                    h3 = 'Lv2'
                elif j == 5:  # Lv1強
                    h3 = 'Lv1'

            if mode == 2 and (j == 4 or j == 6):
                music_list = []
            else:
                music_list = [[h3]]

            # div.table-responsive の tr を走査
            tr_addr = 1  # tr の場所を指定
            while 1:
                try:
                    tr = soup.find_all('div', class_='table-responsive')[i].tbody.find_all('tr')[tr_addr]
                except IndexError:
                    if not music_list:
                        print('music list not found')
                        quit(1)
                    break

                td_list = tr.find_all('td')
                lv = td_list[0].text.strip()
                title = td_list[1].span.text.strip()
                bpm = td_list[2].text.strip()
                music_list.append([lv, title, bpm])

                if not silent:
                    print(title)

                tr_addr += 1

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
