from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from personas.models import Personas
from productos.models import Producto
from .forms import *
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import datetime
import time
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def agregarcompra(request):
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    return render(request, 'compras/agregar.html', {'fecha':fecha})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def listarcompras(request):
    lista = Compra.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'compras/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def agregarcompra2(request):
    if request.method == "GET":
        try:
            c = Compra()
            prov = int(request.GET['proveedor'])
            fact = bool(request.GET['facturado'])
            pago = bool(request.GET['pago'])
            obse = str(request.GET['observacion']).lower()
            nac = request.POST.get('nacimiento')
            f = request.GET['fecha']
            fecha = datetime.datetime.strptime(f, '%d/%m/%Y')
            c.personas = get_object_or_404(Personas, pk=prov)
            c.fecha = fecha
            c.facturado= fact
            c.pago = pago
            c.observacion = obse.lower()
            c.save()
            productos = request.GET.getlist('datos[]')
            for prod in productos:
                p = prod.split(",")
                dc = detalle_compra()
                itempro = get_object_or_404(Producto, pk=p[0])
                dc.producto = itempro
                dc.compra = c
                dc.costo = p[2]
                dc.cantidad = p[1]
                dc.save()
                detalle = "ok"
        except Exception as e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
			return HttpResponse(
				json.dumps(detalle),
				content_type="application/json"
			)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def buscarcompras(request):
    if request.is_ajax():
        texto = request.GET['term'].lower()
        if texto is not None:
            compras = Compra.objects.filter(Q(personas__nombres__contains = texto)|Q(fecha__contains = texto)|Q(observacion__contains = texto))
            for c in compras:
                lista = []
                lista.append({'pk':c.pk, 'proveedor':c.personas.nombres, 'fecha':str(c.fecha), 'pago':c.pago, 'facturado':c.facturado})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def editarcompra(request,pk):
    c = get_object_or_404(Compra, pk=pk)
    productos = list(detalle_compra.objects.filter(compra=pk))
    return render(request, 'compras/editar.html', {'c':c, 'productos':productos})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def eliminarcompra(request, pk):
    c = get_object_or_404(Compra, pk=pk)
    productos = list(detalle_compra.objects.filter(compra=pk))
    detalle = 0
    if request.method == 'POST':
        try:
            print("metodo post")
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(e)
        finally:
            if detalle != 0:
                print(detalle)
                return render(request, 'compras/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('compras_listar'))
    else:
        return render(request, 'compras/eliminar.html', {'c': c, 'productos':productos})
#-------------------------------------------------------------------------------
def rangocompras(fec1, fec2):
    total=0
    lista = Compra.objects.filter(fecha__range=[fec1,fec2])
    for c in lista:
        items = list(detalle_compra.objects.filter(compra=c.pk))
        for i in items:
            total += i.cantidad * i.costo
    return total
