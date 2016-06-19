from django.core.management.base import BaseCommand
import sys

from users.models import CustomUser
from main.models import Bad_Count, Medal, Extra_Option

class Command(BaseCommand):
    help = 'クリアデータを移行します。'

    def handle(self, *args, **options):
        user_from_id = 1    # 移行元
        user_to_id = 2      # 移行先

        # ユーザーオブジェクトを取得
        user_from = CustomUser.objects.get(pk=user_from_id)
        user_to = CustomUser.objects.get(pk=user_to_id)

        # 確認
        print ('"{0}" のクリアデータを "{1}" に移行します。'.format(user_from.username, user_to.username))
        print ('本当によろしいですか？ (Y/n)')
        if input('> ') != 'Y':
            print ('終了します。')
            sys.exit()

        # クリアデータを取得
        medal_list = Medal.objects.filter(user=user_from)
        bad_count_list = Bad_Count.objects.filter(user=user_from)
        extra_option_list = Extra_Option.objects.filter(user=user_from)

        # クリアデータのユーザーを変更
        for medal in medal_list:
            medal.user = user_to
            medal.save()
        for bad_count in bad_count_list:
            bad_count.user = user_to
            bad_count.save()
        for extra_option in extra_option_list:
            extra_option.user = user_to
            extra_option.save()

        print ('\nメダル: {0}'.format(len(medal_list)))
        print ('BAD数: {0}'.format(len(bad_count_list)))
        print ('エクストラオプション: {0}'.format(len(extra_option_list)))
        print ('\n完了しました！')
