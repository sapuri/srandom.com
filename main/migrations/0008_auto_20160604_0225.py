# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-03 17:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160604_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2016, 6, 3, 17, 25, 50, 981204, tzinfo=utc), verbose_name='作成日'),
        ),
    ]
