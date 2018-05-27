#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PersonaForm
from django.core.urlresolvers import reverse_lazy
from .models import Personas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import HttpResponse
from datetime import datetime

@login_required
def listarpersonas(request):
    lista = Personas.objects.all().order_by('nombres')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        personas = paginator.page(page)
    except PageNotAnInteger:
        personas = paginator.page(1)
    except EmptyPage:
        personas = paginator.page(1)
    return render(request, 'personas/listar.html', { 'personas': personas, 'paginator':paginator })

@login_required
def buscarpersonas(request):
    if request.is_ajax():
        texto = request.GET['term'].lower()
        if texto is not None:
            personas = Personas.objects.filter(Q(nombres__contains = texto)|Q(phone__contains = texto)|Q(datos__contains = texto))
            lista = []
            for c in personas:
				lista.append({'pk':c.pk, 'nombres':c.nombres, 'sexo':c.sexo, 'nacimiento':str(c.nacimiento), 'phone':c.phone, 'mayorista':c.mayorista, 'datos':c.datos})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def agregarpersona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Personas()
                c.nombres = form.cleaned_data['nombres'].lower()
                c.datos = form.cleaned_data['datos'].lower()
                c.phone = form.cleaned_data['phone']
                c.sexo = form.cleaned_data['sexo']
                c.mayorista = form.cleaned_data['mayorista']
                c.nacimiento = form.cleaned_data['nacimiento']
                c.save()
        except Exception as e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'personas/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('personas_listar'))
    else:
        form = PersonaForm()
        return render(request, 'personas/agregar.html', {'form': form})

@login_required
def editarpersona(request, pk):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Personas.objects.get(id=pk)
                c.nombres = form.cleaned_data['nombres'].lower()
                c.datos = form.cleaned_data['datos'].lower()
                c.phone = form.cleaned_data['phone']
                c.sexo = form.cleaned_data['sexo']
                c.mayorista = form.cleaned_data['mayorista']
                c.nacimiento = form.cleaned_data['nacimiento']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'personas/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('personas_listar'))
    else:
        c = get_object_or_404(Personas, pk=pk)
        nac = c.nacimiento.strftime("%d/%m/%Y")
        form = PersonaForm(initial={'nombres':c.nombres,
            'datos': c.datos, 'phone':c.phone, 'sexo': c.sexo,
            'mayorista':c.mayorista, 'nacimiento':c.nacimiento.strftime("%d/%m/%Y") })
        return render(request, 'personas/editar.html', {'form': form})

@login_required
def eliminarpersona(request, pk):
    c = get_object_or_404(Personas, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'personas/eliminar.html', {'persona': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('personas_listar'))
    else:
        return render(request, 'personas/eliminar.html', {'persona': c})
