# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-03 17:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20160604_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2016, 6, 4, 2, 2, 28, 371757), verbose_name='作成日'),
        ),
    ]
