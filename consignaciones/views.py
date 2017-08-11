from django.shortcuts import render
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

@login_required
def agregarconsignacion(request):
    return render(request, "consignaciones/agregar.html", {})

@login_required
def listarconsignaciones(request):
    lista = Consignacion.objects.all().order_by('-fecha')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'consignaciones/listar.html', { 'lista': lista, 'paginator':paginator })

@login_required
def agregarconsignacion2(request):
    if request.method == "GET":
        try:
            c = Consignacion()
            clien = int(request.GET['proveedor'])
            obse = str(request.GET['observacion'])
            fecha = datetime.datetime.now()
            c.personas = get_object_or_404(Personas, pk=clien)
            c.fecha = fecha
            c.devuelto = False
            c.pagado = False
            c.observacion = obse
            c.save()
            productos = request.GET.getlist('datos[]')
            for prod in productos:
                p = prod.split(",")
                dc = detalle_consignacion()
                itempro = get_object_or_404(Producto, pk=p[0])
                dc.producto = itempro
                dc.consignacion = c
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
