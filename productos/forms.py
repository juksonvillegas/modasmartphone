from django.forms import *
from .models import *

class CategoriaForm(forms.Form):
    nombre = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese Nombre de categoria'}))

class MarcaForm(forms.Form):
    nombre = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese Nombre de categoria'}))

class ModeloForm(forms.Form):
    nombre = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese Nombre de categoria'}))
    marca = ModelChoiceField(queryset=Marca.objects.all().order_by('nombre'))

class PrecioForm(forms.Form):
    categoria = CharField(widget=HiddenInput)
    modelo = CharField(widget=HiddenInput)
    mayor = DecimalField(decimal_places=2)
    punto = DecimalField(decimal_places=2)
    cliente = DecimalField(decimal_places=2)

class AlmacenForm(forms.Form):
    nombre = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese Nombre de almacen'}))

class ProductoForm(forms.Form):
    categoria = CharField(widget=HiddenInput)
    modelo = CharField(widget=HiddenInput)
    precio = CharField(widget=HiddenInput)
    stock_minimo = IntegerField()

class SkuForm(forms.Form):
    generos = (
        ('varon','Varon'),
        ('mujer','Mujer'),
        ('unisex','Unisex'),
        ('nino','Nino'),
        ('nina','Nina'),
    )
    producto = CharField(widget=HiddenInput)
    imagen = URLField(label="URL de la imagen")
    genero = ChoiceField(choices=(generos))
    descripcion = CharField()

class ExistenciaForm(forms.Form):
    sku = models.ForeignKey('Sku', on_delete=models.CASCADE)
    almacen = models.ForeignKey('Almacen', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
