from django.forms import *
from .models import *
import datetime
from django.forms import *
from productos.models import Producto
from django.core.validators import RegexValidator

def getfecha():
    return datetime.date.today().strftime("%d/%m/%Y")

class PerdidaForm(forms.Form):
    fecha = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
        attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())
    producto = CharField(widget=HiddenInput)
    cantidad = IntegerField()
    observacion = CharField(max_length=50, widget = Textarea(
        attrs={'placeholder':'Ingrese datos extras'}), required=False)
