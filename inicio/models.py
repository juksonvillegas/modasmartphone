from __future__ import unicode_literals
from productos.models import Producto
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.
class Comision(models.Model):
    fecha = models.DateTimeField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comision2producto')
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    observacion = models.CharField(max_length=100)
    def __str__(self):
        return str(self.fecha)

class Caja(models.Model):
    fechaa = models.DateTimeField()
    fechac = models.DateTimeField(null=True, blank=True)
    montoa = models.DecimalField(max_digits=6, decimal_places=2)
    montoc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return str(self.fechaa)

class Avatar(models.Model):
    usuario = models.OneToOneField(User)
    foto = models.URLField(default='http://www.lake-link.com/images/avatars/noAvatar.png')
    def __str__(self):
        return str(self.usuario)
