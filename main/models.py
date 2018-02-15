from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from users.models import CustomUser

class Difficulty(models.Model):
    difficulty = models.CharField('難易度', max_length=10)

    def difficulty_short(self):
        if self.difficulty == 'EXTRA':
            return 'EX'
        elif self.difficulty == 'HYPER':
            return 'H'
        elif self.difficulty == 'NORMAL':
            return 'N'
        elif self.difficulty == 'EASY':
            return 'E'
        else:
            return 'undefined'

    def __str__(self):
        return self.difficulty_short()

    class Meta:
        verbose_name = '難易度'
        verbose_name_plural = '難易度'

class Level(models.Model):
    level = models.IntegerField('レベル')

    # 整数型で返す
    def int(self):
        return self.level

    def __str__(self):
        return str(self.level)

    class Meta:
        verbose_name = 'レベル'
        verbose_name_plural = 'レベル'

class Sran_Level(models.Model):
    level = models.IntegerField('S乱レベル')

    # 整数型で返す
    def int(self):
        return self.level

    def __str__(self):
        return str(self.level)

    class Meta:
        verbose_name = 'S乱レベル'
        verbose_name_plural = 'S乱レベル'

class Music(models.Model):
    title = models.CharField('曲名', max_length=255)
    difficulty = models.ForeignKey(Difficulty, verbose_name='難易度', on_delete=models.PROTECT)
    level = models.ForeignKey(Level, verbose_name='レベル', on_delete=models.PROTECT)
    sran_level = models.ForeignKey(Sran_Level, verbose_name='S乱レベル', on_delete=models.PROTECT)
    bpm = models.CharField('BPM', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '曲'
        verbose_name_plural = '曲'
        indexes = [
            models.Index(fields=['title'], name='title'),
            models.Index(fields=['level'], name='level'),
            models.Index(fields=['sran_level'], name='sran_level'),
        ]

class Medal(models.Model):
    medal = models.IntegerField('クリアメダル')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    # int型で返す
    def int(self):
        return self.medal

    # 文字列で返す
    def output_str(self):
        if self.medal == 1:
            return '金'
        elif self.medal == 2:
            return '銀☆'
        elif self.medal == 3:
            return '銀◇'
        elif self.medal == 4:
            return '銀○'
        elif self.medal == 5:
            return '銅☆'
        elif self.medal == 6:
            return '銅◇'
        elif self.medal == 7:
            return '銅○'
        elif self.medal == 8:
            return '★'
        elif self.medal == 9:
            return '◆'
        elif self.medal == 10:
            return '●'
        elif self.medal == 11:
            return '易'
        elif self.medal == 12:
            return '未プレイ'
        else:
            return ''

    # 更新日時をJSTで返す
    def updated_at_jst(self):
        return self.updated_at + timedelta(hours=9)

    def __str__(self):
        return self.output_str()

    class Meta:
        verbose_name = 'クリアメダル'
        verbose_name_plural = 'クリアメダル'
        indexes = [
            models.Index(fields=['music', 'user'], name='music_user'),
            models.Index(fields=['updated_at'], name='updated_at'),
            models.Index(fields=['user', 'updated_at'], name='user_updated_at'),
        ]

class Bad_Count(models.Model):
    bad_count = models.PositiveIntegerField('BAD数')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    # 整数型で返す
    def int(self):
        return self.bad_count

    def __str__(self):
        return str(self.bad_count)

    # 更新日時をJSTで返す
    def updated_at_jst(self):
        return self.updated_at + timedelta(hours=9)

    class Meta:
        verbose_name = 'BAD数'
        verbose_name_plural = 'BAD数'
        indexes = [
            models.Index(fields=['music', 'user'], name='music_user'),
            models.Index(fields=['updated_at'], name='updated_at'),
            models.Index(fields=['user', 'updated_at'], name='user_updated_at'),
        ]

class Extra_Option(models.Model):
    hard = models.BooleanField('ハード')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    # ハードしているかを判定
    def is_hard(self):
        if self.hard:
            return True
        else:
            False

    # 更新日時をJSTで返す
    def updated_at_jst(self):
        return self.updated_at + timedelta(hours=9)

    class Meta:
        verbose_name = 'Extra Option'
        verbose_name_plural = 'Extra Option'
        indexes = [
            models.Index(fields=['music', 'user'], name='music_user'),
            models.Index(fields=['updated_at'], name='updated_at'),
            models.Index(fields=['user', 'updated_at'], name='user_updated_at'),
        ]

class News(models.Model):
    KIND_CHOICES = (
        ('新規', '新規'),
        ('レベル更新', 'レベル更新'),
        ('S乱レベル更新', 'S乱レベル更新'),
        ('削除', '削除'),
    )

    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.PROTECT)
    kind = models.CharField('種類', max_length=10, choices=KIND_CHOICES)
    created_at = models.DateField('作成日', default=timezone.now)
    status = models.BooleanField('状態', default=True)

    def __str__(self):
        return '%s - %s' % (self.music, self.kind)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

class Activity(models.Model):
    ''' 更新履歴 '''
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)
    status = models.BooleanField('状態', default=True)

    def __str__(self):
        return '%s - %s' % (self.music, self.user)

    class Meta:
        verbose_name = 'アクティビティ'
        verbose_name_plural = 'アクティビティ'
        indexes = [
            models.Index(fields=['music', 'user'], name='music_user'),
        ]
