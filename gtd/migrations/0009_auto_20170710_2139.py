# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 21:39
from __future__ import unicode_literals

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gtd', '0008_auto_20170710_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(blank=True, null=True),
        ),
    ]
