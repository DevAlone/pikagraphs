# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170817_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isRatingBan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='subscribersCount',
            field=models.IntegerField(default=0),
        ),
    ]