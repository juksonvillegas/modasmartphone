from __future__ import unicode_literals
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible



from django.db import models

# Create your models here.
class Personas(models.Model):
    nombres = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=9, blank=True, null=False)
    sexo = models.BooleanField()
    mayorista=models.BooleanField()
    nacimiento = models.DateField(blank=False, null=False)
    datos = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.nombres
