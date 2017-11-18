# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-20 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('gtd', '0013_gtduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='special_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Bin'), (1, 'Collectbox'), (2, 'Actions'),
                                                                        (3, 'Waiting For'), (4, 'Tickler'),
                                                                        (5, 'Someday')], null=True),
        ),
    ]
