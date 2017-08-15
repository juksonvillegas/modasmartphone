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
class Compra(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    fecha = models.DateField()
    facturado = models.BooleanField()
    pago = models.BooleanField()
    observacion = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, through='detalle_compra')

class detalle_compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    costo =  models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField(default=1)

@receiver(post_save, sender=detalle_compra)
def agregarstock(sender, instance, **kwargs):
    if kwargs['created']:
        pk = instance.producto.pk
        nuevo_stock = instance.cantidad
        producto = get_object_or_404(Producto, pk=pk)
        producto.stock+= int(nuevo_stock)
        producto.save()

@receiver(post_delete, sender=detalle_compra)
def quitarstock(sender, instance, **kwargs):
    pk = instance.producto.pk
    nuevo_stock = instance.cantidad
    producto = get_object_or_404(Producto, pk=pk)
    producto.stock-= int(nuevo_stock)
    producto.save()
