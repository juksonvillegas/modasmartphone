from __future__ import unicode_literals
from django.db import models
from personas.models import Personas
from productos.models import Producto
from compras.models import detalle_compra
import datetime
from django.utils import timezone
from django.db.models.signals import *
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

# Create your models here.
class Venta(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    facturado = models.BooleanField()
    efectivo = models.BooleanField()
    observacion = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, through='detalle_venta')
    def __str__(self):
        return self.personas.nombres + str(self.fecha)

class detalle_venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    precio =  models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField(default=1)

def descontardc(prod, cant):
    dcs = detalle_compra.objects.filter(producto=prod, activo=True).order_by('compra__fecha')
    for dc in dcs:
        stock = dc.cantidad - dc.unidades_fuera
        if cant>0:
            if stock >= cant:
                dc.unidades_fuera += int(cant)
                cant = 0
            else:
                cant -= stock
                dc.unidades_fuera = dc.cantidad
            if dc.cantidad == dc.unidades_fuera:
                dc.activo=False
            dc.save()

def regresardc(prod, cant):
        dcs = detalle_compra.objects.filter(producto=prod).order_by('compra__fecha')
        for dc in dcs:
            if cant > 0:
                if cant>dc.unidades_fuera:
                    cant -=dc.unidades_fuera
                else:
                    dc.unidades_fuera -=cant
                    cant = 0
                if dc.cantidad == dc.unidades_fuera:
                    dc.activo = False
                else:
                    dc.activo = True
                dc.save()

@receiver(post_save, sender=detalle_venta)
def descontarstock(sender, instance, **kwargs):
    if kwargs['created']:
        pk = instance.producto.pk
        nuevo_stock = int(instance.cantidad)
        producto = get_object_or_404(Producto, pk=pk)
        producto.stock-= int(nuevo_stock)
        descontardc(producto, nuevo_stock)
        producto.save()

@receiver(post_delete, sender=detalle_venta)
def regresarstock(sender, instance, **kwargs):
    pk = instance.producto.pk
    nuevo_stock = int(instance.cantidad)
    producto = get_object_or_404(Producto, pk=pk)
    producto.stock+= int(nuevo_stock)
    regresardc(producto,nuevo_stock)
    producto.save()
