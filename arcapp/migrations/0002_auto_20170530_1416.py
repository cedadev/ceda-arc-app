# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-30 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arcapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='remote_id',
            field=models.CharField(max_length=200, verbose_name='Remote Job ID'),
        ),
    ]
