# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-16 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0002_auto_20191016_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='can_edit',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='can_edit',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]