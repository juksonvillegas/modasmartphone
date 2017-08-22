from django.forms import *
from .models import *
import datetime
from django.forms import *
from productos.models import Producto
from django.core.validators import RegexValidator

def getfechahora():
    return datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")

def getfecha():
    return datetime.date.today().strftime("%d/%m/%Y")

class ComisionForm(forms.Form):
    fecha = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
         attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())
    producto = CharField(widget=HiddenInput)
    monto = DecimalField(decimal_places=2)
    observacion = CharField(max_length=50, widget = Textarea(
        attrs={'placeholder':'Ingrese datos extras'}), required=False)

class CajaForm(forms.Form):
    fecha = CharField(widget = TextInput(
         attrs={'readonly':'readonly'}), initial = getfechahora())
    monto = DecimalField(decimal_places=2)
