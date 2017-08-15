from __future__ import unicode_literals
from django.db import models
from personas.models import Personas
from productos.models import Producto
import datetime
from django.utils import timezone
from django.db.models.signals import *
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

# Create your models here.
class Consignacion(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    pagado = models.BooleanField(default=False)
    devuelto = models.BooleanField(default=False)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    productos = models.ManyToManyField(Producto, through='detalle_consignacion')
    def __str__(self):
        return self.personas.nombres + str(self.fecha)

class detalle_consignacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    consignacion = models.ForeignKey(Consignacion, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
