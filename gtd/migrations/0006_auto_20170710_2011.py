# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0005_auto_20170710_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionrecurrence',
            name='due_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actionrecurrence',
            name='start_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
