# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mqtt_logger', '0002_mqttsubscription_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mqttmessage',
            options={'verbose_name': 'MQTT message', 'verbose_name_plural': 'MQTT messages'},
        ),
        migrations.AlterModelOptions(
            name='mqttsubscription',
            options={'verbose_name': 'MQTT subscription', 'verbose_name_plural': 'MQTT subscriptions'},
        ),
    ]
