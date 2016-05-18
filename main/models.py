from django.db import models
from datetime import datetime

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
    difficulty = models.ForeignKey(Difficulty, verbose_name='難易度')
    level = models.ForeignKey(Level, verbose_name='レベル')
    sran_level = models.ForeignKey(Sran_Level, verbose_name='S乱レベル')
    bpm = models.CharField('BPM', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '曲'
        verbose_name_plural = '曲'

class Medal(models.Model):
    medal = models.IntegerField('クリアメダル')
    music = models.ForeignKey(Music, verbose_name='曲')
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー')
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
        else:
            return 0

    def __str__(self):
        return self.output_str()

    class Meta:
        verbose_name = 'クリアメダル'
        verbose_name_plural = 'クリアメダル'

class Bad_Count(models.Model):
    bad_count = models.PositiveIntegerField('BAD数')
    music = models.ForeignKey(Music, verbose_name='曲')
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー')
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    # 整数型で返す
    def int(self):
        return self.bad_count

    def __str__(self):
        return str(self.bad_count)

    class Meta:
        verbose_name = 'BAD数'
        verbose_name_plural = 'BAD数'

class Extra_Option(models.Model):
    hard = models.BooleanField('ハード')
    music = models.ForeignKey(Music, verbose_name='曲')
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー')
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    # ハードしているかを判定
    def is_hard(self):
        if self.hard:
            return True
        else:
            False

    class Meta:
        verbose_name = 'Extra Option'
        verbose_name_plural = 'Extra Option'
