# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_perdida'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='costo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]