# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-16 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smelltest', '0004_scent_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='scentgroup',
            name='color',
            field=models.CharField(default='ff0000', max_length=6),
        ),
    ]
