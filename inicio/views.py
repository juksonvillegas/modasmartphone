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
                pk = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk)
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
