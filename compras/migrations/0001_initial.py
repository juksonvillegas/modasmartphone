# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 02:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '__first__'),
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('facturado', models.BooleanField()),
                ('pago', models.BooleanField()),
                ('observacion', models.CharField(max_length=100)),
                ('personas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.Personas')),
            ],
        ),
        migrations.CreateModel(
            name='detalle_compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cantidad', models.IntegerField(default=1)),
                ('unidades_fuera', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.Compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='productos',
            field=models.ManyToManyField(through='compras.detalle_compra', to='productos.Producto'),
        ),
    ]
