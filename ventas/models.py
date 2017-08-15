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
class Venta(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    fecha = models.DateField()
    facturado = models.BooleanField()
    efectivo = models.BooleanField()
    observacion = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, through='detalle_venta')

class detalle_venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    precio =  models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField(default=1)

@receiver(post_save, sender=detalle_venta)
def descontarstock(sender, instance, **kwargs):
    if kwargs['created']:
        pk = instance.producto.pk
        nuevo_stock = instance.cantidad
        producto = get_object_or_404(Producto, pk=pk)
        producto.stock-= int(nuevo_stock)
        producto.save()

@receiver(post_delete, sender=detalle_venta)
def regresarstock(sender, instance, **kwargs):
    pk = instance.producto.pk
    nuevo_stock = instance.cantidad
    producto = get_object_or_404(Producto, pk=pk)
    producto.stock+= int(nuevo_stock)
    producto.save()
