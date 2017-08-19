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
from django.utils.dateparse import parse_date

@login_required
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
