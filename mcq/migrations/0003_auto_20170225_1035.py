# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 10:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0002_auto_20170225_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qattempt',
            old_name='User',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='profile',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 25, 10, 35, 35, 86059, tzinfo=utc)),
        ),
    ]