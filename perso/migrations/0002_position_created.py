# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('perso', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
