from django.core.management.base import BaseCommand

from main.models import Medal
from users.models import CustomUser


class Command(BaseCommand):
    help = 'メダルを1つ以上登録しているユーザーの一覧を表示します。'

    def handle(self, *args, **options):
        user_list = self.get_active_users()
        for user_id in user_list:
            user = CustomUser.objects.get(pk=user_id)
            print(f'https://twitter.com/{user.username}')

    @staticmethod
    def get_active_users():
        return list(set(Medal.objects.values_list('user', flat=True)))
