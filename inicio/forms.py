from django.forms import *
from .models import *
import datetime
from django.forms import *
from productos.models import Producto
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class UsuarioForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    is_staff = BooleanField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', )
