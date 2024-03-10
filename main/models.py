from datetime import datetime

from django.db import models

from users.models import CustomUser


class Difficulty(models.Model):
    difficulty = models.CharField('難易度', max_length=10)

    def difficulty_short(self) -> str:
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

    def __str__(self) -> str:
        return self.difficulty_short()

    class Meta:
        verbose_name = '難易度'
        verbose_name_plural = '難易度'


class Level(models.Model):
    MAX = 50
    MIN = 38

    level = models.IntegerField('レベル')

    def __str__(self) -> str:
        return str(self.level)

    class Meta:
        verbose_name = 'レベル'
        verbose_name_plural = 'レベル'


class Sran_Level(models.Model):
    MAX = 19
    MIN = 1

    level = models.IntegerField('S乱レベル')

    def __str__(self) -> str:
        return str(self.level)

    class Meta:
        verbose_name = 'S乱レベル'
        verbose_name_plural = 'S乱レベル'


class Music(models.Model):
    title = models.CharField('曲名', max_length=255)
    difficulty = models.ForeignKey(Difficulty, verbose_name='難易度', on_delete=models.PROTECT)
    level = models.ForeignKey(Level, verbose_name='レベル', on_delete=models.PROTECT)
    sran_level = models.ForeignKey(Sran_Level, verbose_name='S乱レベル', on_delete=models.PROTECT)
    bpm = models.CharField('BPM', max_length=15, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        verbose_name = '曲'
        verbose_name_plural = '曲'
        indexes = [
            models.Index(fields=['title'], name='title'),
            models.Index(fields=['level'], name='level'),
            models.Index(fields=['sran_level'], name='sran_level'),
        ]


class Medal(models.Model):
    class ClearStatus(models.TextChoices):
        NO_PLAY = 'no-play', 'No Play'
        PERFECT = 'perfect', 'Perfect'
        FULL_COMBO = 'fullcombo', 'Full Combo'
        HARD_CLEARED = 'hard-cleared', 'Hard Cleared'
        CLEARED = 'cleared', 'Cleared'
        FAILED = 'failed', 'Failed'
        EASY_CLEARED = 'easy-cleared', 'Easy Cleared'

    medal = models.IntegerField('クリアメダル')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    def get_clear_status(self, bad_count: 'Bad_Count', extra_option: 'Extra_Option') -> ClearStatus:
        if self.medal == 1 and bad_count.bad_count == 0:
            return self.ClearStatus.PERFECT
        elif 2 <= self.medal <= 4 and bad_count.bad_count == 0:
            return self.ClearStatus.FULL_COMBO
        elif 5 <= self.medal <= 7:
            if extra_option and extra_option.is_hard():
                return self.ClearStatus.HARD_CLEARED
            else:
                return self.ClearStatus.CLEARED
        elif 8 <= self.medal <= 10:
            return self.ClearStatus.FAILED
        elif self.medal == 11:
            return self.ClearStatus.EASY_CLEARED
        else:
            return self.ClearStatus.NO_PLAY

    def __str__(self) -> str:
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

    class Meta:
        verbose_name = 'クリアメダル'
        verbose_name_plural = 'クリアメダル'
        indexes = [
            models.Index(fields=['music', 'user'], name='medal_by_music_and_user'),
            models.Index(fields=['updated_at'], name='medal_by_updated_at'),
            models.Index(fields=['user', 'updated_at'], name='medal_by_user_and_updated_at'),
        ]


class Bad_Count(models.Model):
    bad_count = models.PositiveIntegerField('BAD数')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    def __str__(self) -> str:
        return str(self.bad_count)

    class Meta:
        verbose_name = 'BAD数'
        verbose_name_plural = 'BAD数'
        indexes = [
            models.Index(fields=['music', 'user'], name='bc_by_music_and_user'),
            models.Index(fields=['updated_at'], name='bc_by_updated_at'),
            models.Index(fields=['user', 'updated_at'], name='bc_by_user_and_updated_at'),
        ]


class Extra_Option(models.Model):
    hard = models.BooleanField('ハード')
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)

    def is_hard(self) -> bool:
        if self.hard:
            return True
        return False

    class Meta:
        verbose_name = 'Extra Option'
        verbose_name_plural = 'Extra Option'
        indexes = [
            models.Index(fields=['music', 'user'], name='eo_by_music_user'),
            models.Index(fields=['updated_at'], name='eo_by_updated_at'),
            models.Index(fields=['user', 'updated_at'], name='eo_by_user_and_updated_at'),
        ]


class Activity(models.Model):
    """ 更新履歴 """
    music = models.ForeignKey(Music, verbose_name='曲', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    updated_at = models.DateTimeField('更新日時', default=datetime.now)
    status = models.BooleanField('状態', default=True)

    def __str__(self) -> str:
        return '%s - %s' % (self.music, self.user)

    class Meta:
        verbose_name = 'アクティビティ'
        verbose_name_plural = 'アクティビティ'
        indexes = [
            models.Index(fields=['music', 'user'], name='music_user'),
        ]
