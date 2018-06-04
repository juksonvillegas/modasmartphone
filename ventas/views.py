# -*- coding: utf-8 -*-
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from personas.models import Personas
from productos.models import Producto
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
def agregarventa(request):
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    return render(request, 'ventas/agregar.html', {'fecha':fecha})

@login_required
def listarventas(request):
    lista = Venta.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'ventas/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
def agregarventa2(request):
    if request.method == "GET":
     try:
         c = Venta()
         clie = int(request.GET['cliente'])
         fact = request.GET['facturado']
         pago = request.GET['pago']
         print(pago)
         if fact=='false':
             c.facturado = False
         else:
             c.facturado = True
         if pago=='false':
             c.efectivo = False
         else:
             c.efectivo = True
         print(c.efectivo)
         obse = str(request.GET['observacion'])
         f = request.GET['fecha']
         fecha = datetime.datetime.strptime(f, '%d/%m/%Y')
         c.personas = get_object_or_404(Personas, pk=clie)
         c.fecha = datetime.datetime.now()
         c.observacion = obse
         c.save()
         productos = request.GET.getlist('datos[]')
         for prod in productos:
             p = prod.split(",")
             dc = detalle_venta()
             itempro = get_object_or_404(Producto, pk=p[0])
             dc.producto = itempro
             dc.venta = c
             dc.precio = p[2]
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
def buscarventas(request):
    if request.is_ajax():
     texto = request.GET['term'].lower()
     if texto is not None:
         ventas = Venta.objects.filter(Q(personas__nombres__contains = texto)|Q(fecha__contains = texto)|Q(observacion__contains = texto))
         lista = []
         for c in ventas:
    		lista.append({'pk':c.pk, 'cliente':c.personas.nombres, 'fecha':str(c.fecha), 'pago':c.pago, 'facturado':c.facturado})
         data = json.dumps(lista)
         return HttpResponse(data, content_type='application/json')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def editarventa(request,pk):
    c = get_object_or_404(Venta, pk=pk)
    productos = list(detalle_venta.objects.filter(venta=pk))
    return render(request, 'ventas/editar.html', {'c':c, 'productos':productos})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def eliminarventa(request, pk):
    c = get_object_or_404(Venta, pk=pk)
    productos = list(detalle_venta.objects.filter(venta=pk))
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
             return render(request, 'ventas/eliminar.html', {'c': c, 'detalle':detalle})
         else:
             return redirect(reverse_lazy('ventas_listar'))
    else:
     return render(request, 'ventas/eliminar.html', {'c': c, 'productos':productos})

@login_required
def ventasdiarias(request):
    ventas = Venta.objects.filter(fecha__gte=datetime.date.today()).order_by('-fecha')
    print(ventas)
    #ventas=Venta.objects.all()
    lista = []
    totaldiario = 0
    totalinversion = 0
    totalganancias = 0
    for v in ventas:
        detalles = detalle_venta.objects.filter(venta=v)
        for d in detalles:
            cliente = v.personas
            fecha = v.fecha
            total = d.precio * d.cantidad
            totaldiario +=total
            totalinversion += d.producto.costo * d.cantidad
            ganancia = (d.precio - d.producto.costo) * d.cantidad
            totalganancias += ganancia
            lista.append({'fecha':fecha, 'cliente':cliente, 'precio':d.precio, 'cantidad':d.cantidad, 'producto':d.producto, 'total':total, 'costo':d.producto.costo, 'ganancia':ganancia})
    return render(request, 'ventas/reportes.html', { 'lista': lista, 'totaldiario':totaldiario, 'totalinversion':totalinversion, 'totalganancias':totalganancias})
 #-------------------------------------------------------------------------------
def rangoventas(fec1, fec2):
    total=0
    lista = Venta.objects.filter(fecha__range=[fec1,fec2])
    for c in lista:
        items = list(detalle_venta.objects.filter(venta=c.pk))
        for i in items:
            total += i.cantidad * i.precio
    return total
