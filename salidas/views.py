from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from personas.models import Personas
from productos.models import Producto
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import datetime
import time
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def agregarperdida(request):
    if request.method == 'POST':
        form = PerdidaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Perdida()
                pk = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk)
                c.fecha = form.cleaned_data['fecha']
                c.cantidad = form.cleaned_data['cantidad']
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'salidas/perdidas/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('perdidas_listar'))
    else:
        form = PerdidaForm()
        return render(request, 'salidas/perdidas/agregar.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def listarperdidas(request):
    lista = Perdida.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'salidas/perdidas/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def editarperdida(request, pk):
    if request.method == 'POST':
        form = PerdidaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = get_object_or_404(Perdida, pk=pk)
                pk = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk)
                c.fecha = form.cleaned_data['fecha']
                c.cantidad = form.cleaned_data['cantidad']
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'salidas/perdidas/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('perdidas_listar'))
    else:
        c = get_object_or_404(Perdida, pk=pk)
        nompro = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" + c.producto.modelo.nombre
        form = PerdidaForm(initial={'fecha':c.fecha.strftime("%d/%m/%Y"),
            'producto': c.producto.pk , 'cantidad':c.cantidad, 'observacion': c.observacion})
        return render(request, 'salidas/perdidas/editar.html', {'form': form, 'nompro':nompro})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def eliminarperdida(request, pk):
    c = get_object_or_404(Perdida, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'salidas/perdidas/eliminar.html', {'perdida': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('perdidas_listar'))
    else:
        nompro = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" + c.producto.modelo.nombre
        return render(request, 'salidas/perdidas/eliminar.html', {'c': c, 'nompro':nompro})

#----------------------------------------------------------------------------------------------------

@login_required
def agregargasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Gasto()
                c.fecha = form.cleaned_data['fecha']
                c.monto = form.cleaned_data['monto']
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'salidas/gastos/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('gastos_listar'))
    else:
        form = GastoForm()
        return render(request, 'salidas/gastos/agregar.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def listargastos(request):
    lista = Gasto.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'salidas/gastos/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def editargasto(request, pk):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = get_object_or_404(Gasto, pk=pk)
                c.fecha = form.cleaned_data['fecha']
                c.monto = form.cleaned_data['monto']
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'salidas/gastos/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('gastos_listar'))
    else:
        c = get_object_or_404(Gasto, pk=pk)
        form = GastoForm(initial={'fecha':c.fecha.strftime("%d/%m/%Y"), 'monto':c.monto, 'observacion':c.observacion})
        return render(request, 'salidas/gastos/editar.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def eliminargasto(request, pk):
    c = get_object_or_404(Gasto, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'salidas/gastos/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('gastos_listar'))
    else:
        return render(request, 'salidas/gastos/eliminar.html', {'c': c})
