from __future__ import unicode_literals
from productos.models import Producto
from django.db import models

# Create your models here.
class Comision(models.Model):
    fecha = models.DateField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comision2producto')
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    observacion = models.CharField(max_length=100)
    def __str__(self):
        return str(self.fecha)
