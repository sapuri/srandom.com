from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import sys

from users.models import CustomUser
from main.models import Bad_Count, Medal, Extra_Option

class Command(BaseCommand):
    help = 'クリアデータを移行します。'
    args = '<source_username destination_username>'

    def add_arguments(self, parser):
        # 移行元のユーザー名
        parser.add_argument('username_from', type=str)
        # 移行先のユーザー名
        parser.add_argument('username_to', type=str)

    def handle(self, *args, **options):
        username_from = options['username_from']
        username_to = options['username_to']

        # ユーザーオブジェクトを取得
        try:
            user_from = CustomUser.objects.get(username=username_from)
        except ObjectDoesNotExist:
            print ('移行元のユーザー "{0}" は存在しません。'.format(username_from))
            sys.exit()
        try:
            user_to = CustomUser.objects.get(username=username_to)
        except ObjectDoesNotExist:
            print ('移行先のユーザー "{0}" は存在しません。'.format(username_to))
            sys.exit()

        # 確認
        print ('"{0}" のクリアデータを "{1}" に移行します。'.format(user_from.username, user_to.username))
        print ('本当によろしいですか？ (y/N)')
        if input('> ') != 'y':
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
