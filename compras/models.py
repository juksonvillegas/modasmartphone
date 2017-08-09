from __future__ import unicode_literals
from django.db import models
from personas.models import Personas
from productos.models import Producto
import datetime
from django.utils import timezone

# Create your models here.
hoy = datetime.date.today()
class Compra(models.Model):
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)
    fecha = models.DateField(timezone.now())
    facturado = models.BooleanField()
    pago = models.BooleanField()
    observacion = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto, through='detalle_compra')

class detalle_compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    costo =  models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField(default=1)
