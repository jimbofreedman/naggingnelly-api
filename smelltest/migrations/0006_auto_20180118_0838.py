# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-18 08:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smelltest', '0005_scentgroup_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scentgroup',
            options={'ordering': ['id']},
        ),
    ]
