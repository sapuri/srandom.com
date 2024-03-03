from django.core.management.base import BaseCommand

from main.models import Music, Sran_Level


class Command(BaseCommand):
    help = 'Music モデルの S乱レベルID を反転します。'
    args = '<model_name>'

    def add_arguments(self, parser):
        # 変更するモデル名
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):
        model_name = options['model_name']

        if model_name == 'Sran_Level':
            """Music モデルの S乱レベルID を反転"""
            print('Model: ' + model_name + '\n')
            max_lv = 17
            music_list = Music.objects.all()

            # プレビュー
            print('### プレビュー ###')
            for music in music_list:
                new_sran_level_id = max_lv - music.sran_level.id + 1  # 反転
                print('{0}: {1}({2}) S乱レベルID {3} --> {4}'.format(music.id, music.title, music.difficulty,
                                                                 music.sran_level.id, new_sran_level_id))

            # 確認
            print('\n本当に実行しますか？ (y/N)')
            if input('> ') != 'y':
                print('終了します。')
                quit()

            # 実行
            print('### 実行 ###')
            for music in music_list:
                new_sran_level_id = max_lv - music.sran_level.id + 1
                new_sran_level = Sran_Level.objects.get(pk=new_sran_level_id)
                print('{0}: {1}({2}) S乱レベルID {3} --> {4}'.format(music.id, music.title, music.difficulty,
                                                                 music.sran_level.id, new_sran_level.id))
                music.sran_level = new_sran_level
                music.save()

            print('\n完了しました！')

        else:
            print('不正なモデル名です')
            quit()
