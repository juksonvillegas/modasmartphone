from __future__ import unicode_literals
from productos.models import Modelo
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from personas.models import Personas
# Create your models here.
class Desbloqueo(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    flash = models.BooleanField(default=False)
    imei = models.BooleanField(default=False)
    liberacion = models.BooleanField(default=False)
    cuenta = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    fecha_entregado = models.DateTimeField(blank=True, null=True)
    pagado = models.BooleanField(default=False)
    fecha_pagado = models.DateTimeField(blank=True, null=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.personas.nombres + str(self.fecha) 
