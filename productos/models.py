from __future__ import unicode_literals

from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    marca = models.ForeignKey('Marca',on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    def __str__(self):
        return self.nombre

class Precio(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE)
    mayor = models.DecimalField(max_digits=6, decimal_places=2)
    punto = models.DecimalField(max_digits=6, decimal_places=2)
    cliente = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.categoria.nombre + self.modelo.nombre

class Producto(models.Model):
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    precio = models.ForeignKey('Precio', on_delete=models.CASCADE)
    stock_minimo = models.IntegerField(default=1)
    barra = models.CharField(max_length=8, unique=True, blank=True, null=True)
    descripcion = models.CharField(max_length=70,blank=True, null=True, default="Nada")
    def __str__(self):
        return self.categoria.nombre + self.modelo.nombre

class Almacen(models.Model):
    nombre = models.CharField(max_length=70)
    def __str__(self):
        return self.nombre

class Sku(models.Model):
    generos = (
        ('varon','Varon'),
        ('mujer','Mujer'),
        ('unisex','Unisex'),
        ('nino','Nino'),
        ('nina','Nina'),
    )
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    barra = models.CharField(max_length=8, unique=True, blank=True, null=True)
    #ean-8 inicia en 10 millones quedan 90millones libres
    imagen = models.URLField()
    genero = models.CharField(max_length=15, choices=generos)
    descripcion = models.CharField(max_length=70, default="Nada")
    def __str__(self):
        return self.barra

class Existencias(models.Model):
    sku = models.ForeignKey('Sku', on_delete=models.CASCADE)
    almacen = models.ForeignKey('Almacen', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return self.sku.barra + self.almancen.nombre
