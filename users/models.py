from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    location = models.CharField('都道府県', max_length=10)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = '都道府県'
        verbose_name_plural = '都道府県'

class Theme(models.Model):
    theme = models.CharField('テーマ', max_length=255)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'テーマ'
        verbose_name_plural = 'テーマ'

class CustomUser(AbstractUser):
    player_name = models.CharField('プレイヤー名', max_length=6, null=True, blank=True, help_text='全角ひらがなカタカナ英数字6文字以内')
    poputomo_id = models.CharField('ポプともID', max_length=12, null=True, blank=True, help_text='半角数字12文字')
    location = models.ForeignKey(Location, verbose_name='都道府県', null=True, blank=True, on_delete=models.PROTECT)
    profile = models.TextField('プロフィール', null=True, blank=True)
    player_name_privacy = models.IntegerField('プレイヤー名', default=1, help_text='ランキングにプレイヤー名とプロフィールページへのリンクが掲載されます。(非公開の場合は"匿名希望さん"と表示されます)')
    cleardata_privacy = models.IntegerField('クリアデータ', default=1, help_text='プロフィールページにクリアデータを表示します。')
    updated_recently_privacy = models.IntegerField('最近更新した曲', default=1, help_text='プロフィールページに最近更新した曲を表示します。')
    theme = models.ForeignKey(Theme, verbose_name='テーマ', default=1, on_delete=models.PROTECT)
    premium = models.BooleanField('プレミアムユーザー', default=False, help_text='Amazonギフト券を買ってくれた人')

    def split_poputomo_id(self):
        if self.poputomo_id:
            if len(self.poputomo_id) == 12:
                return self.poputomo_id[0:4] + '-' + self.poputomo_id[4:8] + '-' + self.poputomo_id[8:12]
