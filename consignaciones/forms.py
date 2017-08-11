from django.forms import *
from .models import *
import datetime

class ConsignacionForm(forms.Form):
    personas = CharField(widget=HiddenInput)

class Detalle_ConsignacionForm(forms.Form):
    producto = CharField(widget=HiddenInput)
    cantidad = IntegerField()
