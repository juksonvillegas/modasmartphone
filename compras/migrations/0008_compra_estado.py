# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-11 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_auto_20170810_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
