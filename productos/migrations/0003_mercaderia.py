# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-10 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_auto_20170727_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mercaderia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_minimo', models.IntegerField(default=1)),
                ('barra', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('descripcion', models.CharField(default='Nada', max_length=70)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Categoria')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Modelo')),
                ('precio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Precio')),
            ],
        ),
    ]
