# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-16 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smelltest', '0003_scentgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='scent',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smelltest.ScentGroup'),
            preserve_default=False,
        ),
    ]
