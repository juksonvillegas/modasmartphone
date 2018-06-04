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
from personas.models import Personas
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test

#if not request.user.is_anonymous():
        #return HttpResponseRedirect('/privado')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/caja/listar')
def agregarusuario(request):
    if request.method == 'POST':
        group_admin, created = Group.objects.get_or_create(name='administrador')
        group_vendedor, created2 = Group.objects.get_or_create(name='vendedor')
        form = UsuarioForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                if(form.cleaned_data['password1']==form.cleaned_data['password2']):
                    c = User()
                    c.first_name = form.cleaned_data['first_name']
                    c.last_name = form.cleaned_data['last_name']
                    c.username = form.cleaned_data['username']
                    c.email = form.cleaned_data['email']
                    c.set_password(form.cleaned_data['password1'])
                    c.is_staff = form.cleaned_data['is_staff']
                    c.save()
                    if c.is_staff==True:
                        c.groups.add(group_admin)
                    else:
                        c.groups.add(group_vendedor)
                    c.save()
                else:
                    detalle="Password diferentes"
        except Exception as e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/usuario/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('personas_listar'))
    else:
        form = UsuarioForm()
        return render(request, 'inicio/usuario/agregar.html', {'form': form})


@login_required
def agregarcomision(request):
    if request.method == 'POST':
        form = ComisionForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Comision()
                c.fecha = form.cleaned_data['fecha']
                if c.fecha.strftime("%d/%m/%Y") == datetime.date.today().strftime("%d/%m/%Y"):
                    print("entro")
                    c.fecha = datetime.datetime.now()
                c.monto = form.cleaned_data['monto']
                clie = form.cleaned_data['personas']
                pk1 = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk1)
                c.personas = get_object_or_404(Personas, pk=clie)
                c.observacion = form.cleaned_data['observacion']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                print(detalle, form.data['fecha'])
                return render(request, 'inicio/comisiones/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('comisiones_listar'))
    else:
        form = ComisionForm()
        return render(request, 'inicio/comisiones/agregar.html', {'form': form})

@login_required
def listarcomisiones(request):
    lista = Comision.objects.filter(fecha__gte=datetime.date.today()).order_by('-fecha')
    total = 0
    for l in lista:
        total += l.monto
    page = request.GET.get('page')
    paginator = Paginator(lista, 20)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'inicio/comisiones/listar.html', { 'lista': lista, 'paginator':paginator, 'total':total })

@login_required
def rankingcomisiones(request):
    listapersonas = Personas.objects.all()
    lista=[]
    #lista = Comision.objects.all().order_by('personas')
    for p in listapersonas:
        comisionxpersona = Comision.objects.filter(personas=p)
        totalpersona=0
        for c in comisionxpersona:
            totalpersona+=c.monto
        lista.append({'persona':p.nombres, 'total':totalpersona})
    lista=sorted(lista, key=lambda k: k['total'], reverse=True)
    page = request.GET.get('page')
    paginator = Paginator(lista, 20)
    try:
        lista = paginator.page(page)
    except PageNotAnInteger:
        lista = paginator.page(1)
    except EmptyPage:
        lista = paginator.page(1)
    return render(request, 'inicio/comisiones/ranking.html', { 'lista': lista, 'paginator':paginator })

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
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'inicio/comisiones/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('comisiones_listar'))
    else:
        c = get_object_or_404(Comision, pk=pk)
        id_producto = c.producto.pk
        id_cliente = c.personas.pk
        nompro = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" + c.producto.modelo.nombre
        cliente = c.personas.nombres
        print(cliente)
        form = ComisionForm(initial={'producto':id_producto ,'fecha':c.fecha.strftime("%d/%m/%Y"), 'monto':c.monto, 'observacion':c.observacion})
        return render(request, 'inicio/comisiones/editar.html', {'form': form, 'nompro':nompro})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
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
def reportecomisiones(request):
    if request.method == 'POST':
        form = ReporteComisionForm(request.POST)
        detalle = 0
        total = 0
        paginator = None
        try:
            if form.is_valid():
                fechainicio = form.cleaned_data['fechainicio']
                fechafin = form.cleaned_data['fechafin']
                f1 = fechainicio.strftime("%Y-%m-%d")
                f2 = fechafin.strftime("%Y-%m-%d")
                lista = Comision.objects.filter(fecha__range=[f1,f2])
                for c in lista:
                    total += c.monto
                page = request.GET.get('page')
                paginator = Paginator(lista, 50)
                try:
                    lista = paginator.page(page)
                except PageNotAnInteger:
                    lista = paginator.page(1)
                except EmptyPage:
                    lista = paginator.page(1)
        except Exception, e:
            lista = 0
            detalle = "Error: " + str(e)
        finally:
            return render(request, 'inicio/comisiones/reportes.html', {'total': total, 'detalle':detalle, 'form':form,'lista':lista, 'paginator':paginator})
    else:
        total = 0
        form = ReporteComisionForm()
        return render(request, 'inicio/comisiones/reportes.html', {'form':form})

@login_required
def reportecomsionpersona(request):
    if request.method == 'POST':
        form = ComisionPersonaForm(request.POST)
        detalle = 0
        total = 0
        try:
            if form.is_valid():
                clie = form.cleaned_data['personas']
                persona = get_object_or_404(Personas, pk=clie)
                lista = Comision.objects.filter(personas=persona)
                for c in lista:
                    total += c.monto
        except Exception, e:
            lista = 0
            detalle = "Error: " + str(e)
        finally:
            return render(request, 'inicio/comisiones/reportepersona.html', {'total': total, 'detalle':detalle, 'form':form,'lista':lista})
    else:
        total = 0
        form = ComisionPersonaForm()
        return render(request, 'inicio/comisiones/reportepersona.html', {'form':form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
def abrircaja(request):
    if request.method == 'POST':
        form = CajaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Caja()
                c.montoa = form.cleaned_data['monto']
                c.fechaa = datetime.datetime.utcnow()
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
@user_passes_test(lambda u: u.is_staff, login_url='/consignaciones/listar')
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
