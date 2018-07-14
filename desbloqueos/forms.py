from django.forms import *
from .models import *
import datetime
from django.forms import *
from productos.models import Modelo
from personas.models import Personas
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class DesbloqueoForm(forms.Form):
    personas = CharField(widget=HiddenInput)
    modelo = CharField(widget=HiddenInput)
    monto = DecimalField(decimal_places=2)
    flash = BooleanField(required=False)
    imei = BooleanField(required=False)
    liberacion = BooleanField(required=False)
    cuenta = BooleanField(required=False)
    entregado = BooleanField(required=False)
    pagado = BooleanField(required=False)
    observacion = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese datos extras'}), required=False)

def getfecha():
    return datetime.date.today().strftime("%d/%m/%Y")

class DesbloqueoFechaForm(forms.Form):
    fechainicio = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
             attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())
    fechafin = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
             attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())
