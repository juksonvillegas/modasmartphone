# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-22 00:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0008_perdida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=6)),
                ('observacion', models.CharField(max_length=100)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comision2producto', to='productos.Producto')),
            ],
        ),
    ]
