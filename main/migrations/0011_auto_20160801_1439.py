# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20160604_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='kind',
            field=models.CharField(choices=[('新規', '新規'), ('レベル更新', 'レベル更新'), ('S乱レベル更新', 'S乱レベル更新'), ('削除', '削除')], max_length=10, verbose_name='種類'),
        ),
    ]
