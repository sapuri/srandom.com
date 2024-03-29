# Generated by Django 3.2.7 on 2022-09-24 12:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(max_length=10, verbose_name='難易度')),
            ],
            options={
                'verbose_name': '難易度',
                'verbose_name_plural': '難易度',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(verbose_name='レベル')),
            ],
            options={
                'verbose_name': 'レベル',
                'verbose_name_plural': 'レベル',
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='曲名')),
                ('bpm', models.CharField(blank=True,
                 max_length=15, null=True, verbose_name='BPM')),
                ('difficulty', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.difficulty', verbose_name='難易度')),
                ('level', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.level', verbose_name='レベル')),
            ],
            options={
                'verbose_name': '曲',
                'verbose_name_plural': '曲',
            },
        ),
        migrations.CreateModel(
            name='Sran_Level',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(verbose_name='S乱レベル')),
            ],
            options={
                'verbose_name': 'S乱レベル',
                'verbose_name_plural': 'S乱レベル',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('新規', '新規'), ('レベル更新', 'レベル更新'), (
                    'S乱レベル更新', 'S乱レベル更新'), ('削除', '削除')], max_length=10, verbose_name='種類')),
                ('created_at', models.DateField(
                    default=django.utils.timezone.now, verbose_name='作成日')),
                ('status', models.BooleanField(default=True, verbose_name='状態')),
                ('music', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.music', verbose_name='曲')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.AddField(
            model_name='music',
            name='sran_level',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='main.sran_level', verbose_name='S乱レベル'),
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('medal', models.IntegerField(verbose_name='クリアメダル')),
                ('updated_at', models.DateTimeField(
                    default=datetime.datetime.now, verbose_name='更新日時')),
                ('music', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.music', verbose_name='曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': 'クリアメダル',
                'verbose_name_plural': 'クリアメダル',
            },
        ),
        migrations.CreateModel(
            name='Extra_Option',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('hard', models.BooleanField(verbose_name='ハード')),
                ('updated_at', models.DateTimeField(
                    default=datetime.datetime.now, verbose_name='更新日時')),
                ('music', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.music', verbose_name='曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': 'Extra Option',
                'verbose_name_plural': 'Extra Option',
            },
        ),
        migrations.CreateModel(
            name='Bad_Count',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('bad_count', models.PositiveIntegerField(verbose_name='BAD数')),
                ('updated_at', models.DateTimeField(
                    default=datetime.datetime.now, verbose_name='更新日時')),
                ('music', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.music', verbose_name='曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': 'BAD数',
                'verbose_name_plural': 'BAD数',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(
                    default=datetime.datetime.now, verbose_name='更新日時')),
                ('status', models.BooleanField(default=True, verbose_name='状態')),
                ('music', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='main.music', verbose_name='曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': 'アクティビティ',
                'verbose_name_plural': 'アクティビティ',
            },
        ),
        migrations.AddIndex(
            model_name='music',
            index=models.Index(fields=['title'], name='title'),
        ),
        migrations.AddIndex(
            model_name='music',
            index=models.Index(fields=['level'], name='level'),
        ),
        migrations.AddIndex(
            model_name='music',
            index=models.Index(fields=['sran_level'], name='sran_level'),
        ),
        migrations.AddIndex(
            model_name='medal',
            index=models.Index(
                fields=['music', 'user'], name='medal_by_music_and_user'),
        ),
        migrations.AddIndex(
            model_name='medal',
            index=models.Index(fields=['updated_at'],
                               name='medal_by_updated_at'),
        ),
        migrations.AddIndex(
            model_name='medal',
            index=models.Index(
                fields=['user', 'updated_at'], name='medal_by_user_and_updated_at'),
        ),
        migrations.AddIndex(
            model_name='extra_option',
            index=models.Index(
                fields=['music', 'user'], name='eo_by_music_user'),
        ),
        migrations.AddIndex(
            model_name='extra_option',
            index=models.Index(fields=['updated_at'], name='eo_by_updated_at'),
        ),
        migrations.AddIndex(
            model_name='extra_option',
            index=models.Index(
                fields=['user', 'updated_at'], name='eo_by_user_and_updated_at'),
        ),
        migrations.AddIndex(
            model_name='bad_count',
            index=models.Index(
                fields=['music', 'user'], name='bc_by_music_and_user'),
        ),
        migrations.AddIndex(
            model_name='bad_count',
            index=models.Index(fields=['updated_at'], name='bc_by_updated_at'),
        ),
        migrations.AddIndex(
            model_name='bad_count',
            index=models.Index(
                fields=['user', 'updated_at'], name='bc_by_user_and_updated_at'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['music', 'user'], name='music_user'),
        ),
    ]
