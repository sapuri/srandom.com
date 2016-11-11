from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import sys

from users.models import CustomUser
from main.models import Bad_Count, Medal, Extra_Option

class Command(BaseCommand):
    help = '指定されたアカウントを削除します。'
    args = '<username>'

    def add_arguments(self, parser):
        # 削除するアカウントのユーザー名
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']

        # ユーザーオブジェクトを取得
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            print ('ユーザー "{0}" は存在しません。'.format(username))
            sys.exit()

        # クリアデータ数を取得
        medal_num = Medal.objects.filter(user=user).count()
        bad_count_num = Bad_Count.objects.filter(user=user).count()
        extra_option_num = Extra_Option.objects.filter(user=user).count()

        # 確認
        print ('アカウント "{0}" を削除します。'.format(user.username))
        print ('アカウントが無効になり、これらのクリアデータは完全に削除されます。')
        print ('メダル: {0} 件'.format(medal_num))
        print ('BAD数: {0} 件'.format(bad_count_num))
        print ('エクストラオプション: {0} 件'.format(extra_option_num))
        print ('\n本当によろしいですか？ (y/N)')
        if input('> ') != 'y':
            print ('終了します。')
            sys.exit()

        # 全クリアデータを削除
        medal_list = Medal.objects.filter(user=user).delete()
        bad_count_list = Bad_Count.objects.filter(user=user).delete()
        extra_option_list = Extra_Option.objects.filter(user=user).delete()

        # アカウントを無効化
        user.is_active = False
        user.save()

        print ('\n完了しました！')
