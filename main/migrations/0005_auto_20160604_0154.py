# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-03 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160604_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='作成日'),
        ),
    ]