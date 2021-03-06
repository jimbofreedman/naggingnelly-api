# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-16 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smelltest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='result',
        ),
        migrations.AddField(
            model_name='testresult',
            name='guess',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='guesses', to='smelltest.Scent'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testresult',
            name='scent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='smelltest.Scent'),
        ),
    ]
