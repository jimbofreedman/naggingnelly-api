# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-02 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0017_auto_20180108_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='color',
            field=models.CharField(default='ffffff', max_length=6),
        ),
    ]
