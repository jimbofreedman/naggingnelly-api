# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-08 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0015_auto_20180102_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]
