from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from personas.models import Personas
from productos.models import Producto
from .forms import *
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
def agregardesbloqueo(request):
    if request.method == 'POST':
        form = DesbloqueoForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Desbloqueo()
                c.fecha = datetime.datetime.now()
                c.monto = form.cleaned_data['monto']
                clie = form.cleaned_data['personas']
                pk1 = form.cleaned_data['modelo']
                c.modelo = get_object_or_404(Modelo, pk=pk1)
                c.personas = get_object_or_404(Personas, pk=clie)
                c.observacion = form.cleaned_data['observacion']
                flash = bool(form.cleaned_data['flash'])
                imei = bool(form.cleaned_data['imei'])
                liberacion = bool(form.cleaned_data['liberacion'])
                cuenta = bool(form.cleaned_data['cuenta'])
                c.flash = flash
                c.imei = imei
                c.liberacion = liberacion
                c.cuenta = cuenta
                entregado = bool(form.cleaned_data['entregado'])
                pagado = bool(form.cleaned_data['pagado'])
                print(entregado, pagado)
                c.entregado = entregado
                c.pagado = pagado
                if c.entregado:
                    c.fecha_entregado = datetime.datetime.now()
                if c.pagado:
                    c.fecha_pagado = datetime.datetime.now()
                c.save()
        except Exception as e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                print(detalle)
                return render(request, 'desbloqueos/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('desbloqueos_listar'))
    else:
        form = DesbloqueoForm()
        return render(request, 'desbloqueos/agregar.html', {'form': form})

@login_required
def listardesbloqueos(request):
    lista = Desbloqueo.objects.filter(pagado=False).order_by('-fecha')
    total = 0
    for l in lista:
        total += l.monto
    page = request.GET.get('page')
    paginator = Paginator(lista, 30)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'desbloqueos/listar.html', { 'lista': lista, 'paginator':paginator, 'total':total})

@login_required
def listardesbloqueoscobrados(request):
    lista = Desbloqueo.objects.filter(pagado=True, fecha_pagado__gte=datetime.date.today()).order_by('-fecha')
    total = 0
    for l in lista:
        total += l.monto
    page = request.GET.get('page')
    paginator = Paginator(lista, 30)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'desbloqueos/listarcobrados.html', { 'lista': lista, 'paginator':paginator, 'total':total})


@login_required
def entregardesbloqueo(request, pk):
    c = get_object_or_404(Desbloqueo, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.entregado = True
            c.fecha_entregado = datetime.datetime.now()
            c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'desbloqueos/entregar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('desbloqueos_listar'))
    else:
        modelo = c.modelo.marca.nombre + '-' +  c.modelo.nombre
        cliente = c.personas.nombres
        return render(request, 'desbloqueos/entregar.html', {'c': c, 'modelo':modelo, 'cliente':cliente})

@login_required
def cobrardesbloqueo(request, pk):
    c = get_object_or_404(Desbloqueo, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            if c.entregado != True:
                c.entregado = True
                c.fecha_entregado = datetime.datetime.now()
            c.pagado = True
            c.fecha_pagado = datetime.datetime.now()
            c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'desbloqueos/cobrar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('desbloqueos_listar'))
    else:
        modelo = c.modelo.marca.nombre + '-' +  c.modelo.nombre
        cliente = c.personas.nombres
        return render(request, 'desbloqueos/cobrar.html', {'c': c, 'modelo':modelo, 'cliente':cliente})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def eliminardesbloqueo(request, pk):
    c = get_object_or_404(Desbloqueo, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'desbloqueos/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('desbloqueos_listar'))
    else:
        modelo = c.modelo.marca.nombre + '-' +  c.modelo.nombre
        cliente = c.personas.nombres
        return render(request, 'desbloqueos/eliminar.html', {'c': c, 'modelo':modelo, 'cliente':cliente})
