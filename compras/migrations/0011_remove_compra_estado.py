# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-11 21:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0010_auto_20170811_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='estado',
        ),
    ]
