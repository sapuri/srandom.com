# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-25 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20160525_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=255, verbose_name='テーマ')),
            ],
            options={
                'verbose_name_plural': 'テーマ',
                'verbose_name': 'テーマ',
            },
        ),
    ]