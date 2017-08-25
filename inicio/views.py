from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import datetime
import time

class principal(LoginRequiredMixin, TemplateView):
    template_name = "inicio/base.html"

@login_required
def agregarcomision(request):
    if request.method == 'POST':
        form = ComisionForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Comision()
                c.fecha = form.cleaned_data['fecha']
                c.monto = form.cleaned_data['monto']
                pk1 = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk1)
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/comisiones/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('comisiones_listar'))
    else:
        form = ComisionForm()
        return render(request, 'inicio/comisiones/agregar.html', {'form': form})

@login_required
def listarcomisiones(request):
    lista = Comision.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'inicio/comisiones/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
def editarcomision(request, pk):
    if request.method == 'POST':
        form = ComisionForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = get_object_or_404(Comision, pk=pk)
                pk1 = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk1)
                c.fecha = form.cleaned_data['fecha']
                c.monto = form.cleaned_data['monto']
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/comisiones/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('comisiones_listar'))
    else:
        c = get_object_or_404(Comision, pk=pk)
        id_producto = c.producto.pk
        nompro = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" + c.producto.modelo.nombre
        form = ComisionForm(initial={'producto':id_producto ,'fecha':c.fecha.strftime("%d/%m/%Y"), 'monto':c.monto, 'observacion':c.observacion})
        return render(request, 'inicio/comisiones/editar.html', {'form': form, 'nompro':nompro})

@login_required
def eliminarcomision(request, pk):
    c = get_object_or_404(Comision, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'inicio/comisiones/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('comisiones_listar'))
    else:
        nompro = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" + c.producto.modelo.nombre
        return render(request, 'inicio/comisiones/eliminar.html', {'c': c, 'nompro':nompro})

@login_required
def listarcajas(request):
    lista = Caja.objects.all().order_by('-fechaa')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'inicio/caja/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
def abrircaja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Caja()
                c.montoa = form.cleaned_data['monto']
                c.fechaa = datetime.datetime.now()
                c.usuario = request.user
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/caja/abrir.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('caja_listar'))
    else:
        unlock = False
        try:
            c = Caja.objects.latest('estado')
            if c.estado:
                unlock=True
            else:
                unlock = False
        except Caja.DoesNotExsist:
            unlock = False
        finally:
            form = CajaForm()
            return render(request, 'inicio/caja/abrir.html', {'form': form, 'unlock':unlock})

@login_required
def cerrarcaja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Caja.objects.get(estado=True)
                c.montoc = form.cleaned_data['monto']
                c.fechac = datetime.datetime.now()
                c.usuario = request.user
                c.estado = False
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/caja/cerrar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('caja_listar'))
    else:
        c="vacio"
        try:
            c = Caja.objects.get(estado=True)
        except Caja.DoesNotExsist:
            c = "vacio"
        finally:
            form = CajaForm()
            return render(request, 'inicio/caja/cerrar.html', {'form': form, 'c':c})
