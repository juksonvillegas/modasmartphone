from django.forms import *
from .models import *
import datetime
from django.forms import *
from productos.models import Producto
from personas.models import Personas
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import pytz

def getfechahora():
    lima_now = datetime.datetime.now(pytz.timezone("America/Lima")).strftime("%d/%m/%Y-%H:%M")
    return lima_now

def getfecha():
    return datetime.date.today().strftime("%d/%m/%Y")

class ComisionForm(forms.Form):
    fecha = DateTimeField(input_formats=['%d/%m/%Y'],widget = TextInput(
         attrs={'placeholder':'dd/mm/aaaa'}), initial = getfechahora())
    producto = CharField(widget=HiddenInput)
    personas = CharField(widget=HiddenInput)
    monto = DecimalField(decimal_places=2)
    observacion = CharField(max_length=50, widget = Textarea(
        attrs={'placeholder':'Ingrese datos extras'}), required=False)

class ComisionPersonaForm(forms.Form):
    personas = CharField(widget=HiddenInput)

class ReporteComisionForm(forms.Form):
    fechainicio = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
             attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())
    fechafin = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
             attrs={'placeholder':'dd/mm/aaaa'}), initial = getfecha())

class CajaForm(forms.Form):
    fecha = CharField(widget = TextInput(
         attrs={'readonly':'readonly'}), initial = getfechahora())
    monto = DecimalField(decimal_places=2)

class UsuarioForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    is_staff = BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', )
