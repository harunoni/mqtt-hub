# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mqtt_logger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mqttsubscription',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]