from __future__ import unicode_literals
from django.db.models.signals import *
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db import models
from productos.models import Producto

# Create your models here.
class Perdida(models.Model):
    fecha = models.DateField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='Perdida2producto')
    cantidad = models.IntegerField(default=1)
    observacion = models.CharField(max_length=100)
    def __str__(self):
        return str(self.fecha)

class Egreso(models.Model):
    fecha = models.DateField()
    monto =  models.DecimalField(max_digits=6, decimal_places=2)
    observacion = models.CharField(max_length=100)
    def __str__(self):
        return str(self.fecha)

class Pago(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    acreedor = models.CharField(max_length=70)
    vencido = models.BooleanField(default=False)
    pagado = models.BooleanField(default=False)
    observacion = models.CharField(max_length=50)
    def __str__(self):
        return self.acreedor + str(self.fecha)

class Gasto(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    observacion = models.CharField(max_length=50)
    def __str__(self):
        return str(self.fecha)

@receiver(post_save, sender=Perdida)
def descontarstock(sender, instance, **kwargs):
    if kwargs['created']:
        pk = instance.producto.pk
        nuevo_stock = instance.cantidad
        producto = get_object_or_404(Producto, pk=pk)
        producto.stock-= int(nuevo_stock)
        producto.save()
