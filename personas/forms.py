from django import forms
from django.db import models
from django.forms import *
from .models import Personas
from django.core.validators import RegexValidator

opciones_sexo = ((True, "Hombre"),(False, "Mujer"))
opciones_mayorista = ((True, "Mayorista"),(False, "Normal"))

class PersonaForm(forms.Form):
    nombres = CharField(max_length=50, widget = TextInput(
        attrs={'placeholder':'Ingrese Nombres completos'}))
    phone = CharField(widget=TextInput(attrs={'placeholder':'Ingrese telefono'}))
    sexo = ChoiceField(choices=opciones_sexo, required=True)
    mayorista = ChoiceField(choices=opciones_mayorista, required=True)
    nacimiento = DateField(input_formats=['%d/%m/%Y'],widget = TextInput(
        attrs={'placeholder':'dd/mm/aaaa'}))
    datos = CharField(max_length=50, widget = Textarea(
        attrs={'placeholder':'Ingrese datos extras'}), required=False)
