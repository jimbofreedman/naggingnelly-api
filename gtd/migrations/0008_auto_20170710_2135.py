# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 21:35
from __future__ import unicode_literals

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0007_auto_20170710_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
