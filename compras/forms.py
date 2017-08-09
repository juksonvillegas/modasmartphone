from django.forms import *
from .models import *
import datetime

def getfecha():
    return datetime.date.today().strftime("%d/%m/%Y")

class CompraForm(forms.Form):
    personas = CharField(widget=HiddenInput)
    fecha = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
        attrs={'placeholder':'dd/mm/aaaa'}), initial=getfecha())
    facturado = BooleanField()
    pago = BooleanField(initial=True)
    observacion = CharField(max_length=50, widget = Textarea(
        attrs={'placeholder':'Ingrese datos extras', 'rows':'2'}))
    attrs = {'class': 'hide', 'size': '40'}

class Detalle_CompraForm(forms.Form):
    producto = CharField(widget=HiddenInput)
    costo = DecimalField(decimal_places=2)
    cantidad = IntegerField()
