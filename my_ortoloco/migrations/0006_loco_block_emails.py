# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-30 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ortoloco', '0005_taetigkeitsbereich_show_coordinator_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='loco',
            name='block_emails',
            field=models.BooleanField(default=False, verbose_name=b'keine emails'),
        ),
    ]