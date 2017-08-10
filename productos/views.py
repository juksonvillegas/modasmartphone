from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
from django.http import HttpResponse
from decimal import Decimal

@login_required
def agregarcategoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Categoria()
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/categorias/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('categorias_listar'))
    else:
        form = CategoriaForm()
        return render(request, 'productos/categorias/agregar.html', {'form': form})

@login_required
def listarcategorias(request):
    lista = Categoria.objects.all().order_by('nombre')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/categorias/listar.html', { 'categorias': clase, 'paginator':paginator })

@login_required
def buscarcategorias(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Categoria.objects.filter(Q(nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'nombre':c.nombre})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarcategorias(request, pk):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Categoria.objects.get(id=pk)
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/categorias/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('categorias_listar'))
    else:
        c = get_object_or_404(Categoria, pk=pk)
        form = CategoriaForm(initial={'nombre':c.nombre})
        return render(request, 'productos/categorias/editar.html', {'form': form})

@login_required
def eliminarcategorias(request, pk):
    c = get_object_or_404(Categoria, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/categorias/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('categorias_listar'))
    else:
        return render(request, 'productos/categorias/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------

@login_required
def agregarmarca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Marca()
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/marcas/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('marcas_listar'))
    else:
        form = MarcaForm()
        return render(request, 'productos/marcas/agregar.html', {'form': form})

@login_required
def listarmarcas(request):
    lista = Marca.objects.all().order_by('nombre')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/marcas/listar.html', { 'marcas': clase, 'paginator':paginator })

@login_required
def buscarmarcas(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Marca.objects.filter(Q(nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'nombre':c.nombre})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarmarcas(request, pk):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Marca.objects.get(id=pk)
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/marcas/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('marcas_listar'))
    else:
        c = get_object_or_404(Marca, pk=pk)
        form = MarcaForm(initial={'nombre':c.nombre})
        return render(request, 'productos/marcas/editar.html', {'form': form})

@login_required
def eliminarmarcas(request, pk):
    c = get_object_or_404(Marca, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/marcas/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('marcas_listar'))
    else:
        return render(request, 'productos/marcas/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------
@login_required
def agregarmodelo(request):
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Modelo()
                c.nombre = form.cleaned_data['nombre']
                c.marca = form.cleaned_data['marca']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/modelos/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('modelos_listar'))
    else:
        form = ModeloForm()
        return render(request, 'productos/modelos/agregar.html', {'form': form})

@login_required
def listarmodelos(request):
    lista = Modelo.objects.all().order_by('nombre')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/modelos/listar.html', { 'modelos': clase, 'paginator':paginator })

@login_required
def buscarmodelos(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Modelo.objects.filter(Q(nombre__contains = texto)| Q(marca__nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'nombre':c.nombre, 'marca': c.marca.nombre})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarmodelos(request, pk):
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Modelo.objects.get(id=pk)
                c.nombre = form.cleaned_data['nombre']
                c.marca = form.cleaned_data['marca']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/modelos/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('modelos_listar'))
    else:
        c = get_object_or_404(Modelo, pk=pk)
        form = ModeloForm(initial={'nombre':c.nombre, 'marca':c.marca})
        return render(request, 'productos/modelos/editar.html', {'form': form})

@login_required
def eliminarmodelos(request, pk):
    c = get_object_or_404(Modelo, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/modelos/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('modelos_listar'))
    else:
        return render(request, 'productos/modelos/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------
@login_required
def agregarprecio(request):
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Precio()
                pk2 = form.cleaned_data['categoria']
                pk1 = form.cleaned_data['modelo']
                c.categoria = get_object_or_404(Categoria, pk=pk2)
                c.modelo = get_object_or_404(Modelo, pk=pk1)
                c.mayor = form.cleaned_data['mayor']
                c.punto = form.cleaned_data['punto']
                c.cliente = form.cleaned_data['cliente']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/precios/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('precios_listar'))
    else:
        form = PrecioForm()
        return render(request, 'productos/precios/agregar.html', {'form': form})

@login_required
def listarprecios(request):
    lista = Precio.objects.all().order_by('categoria')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/precios/listar.html', { 'lista': clase, 'paginator':paginator })

@login_required
def buscarprecios(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Precio.objects.filter(Q(categoria__nombre__contains = texto)| Q(modelo__marca__nombre__contains = texto)| Q(modelo__nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'categoria':c.categoria.nombre, 'modelo':c.modelo.nombre, 'mayor':str(c.mayor), 'punto':str(c.punto), 'cliente':str(c.cliente)})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarprecios(request, pk):
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Precio.objects.get(id=pk)
                pk2 = form.cleaned_data['categoria']
                pk1 = form.cleaned_data['modelo']
                c.categoria = get_object_or_404(Categoria, pk=pk2)
                c.modelo = get_object_or_404(Modelo, pk=pk1)
                c.mayor = form.cleaned_data['mayor']
                c.punto = form.cleaned_data['punto']
                c.cliente = form.cleaned_data['cliente']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/precios/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('precios_listar'))
    else:
        c = get_object_or_404(Precio, pk=pk)
        form = PrecioForm(initial={'categoria':c.categoria.pk,'modelo':c.modelo.pk, 'mayor':c.mayor, 'punto':c.punto, 'cliente':c.cliente})
        modnom = c.modelo.marca.nombre + "-" +  c.modelo.nombre
        return render(request, 'productos/precios/editar.html', {'form': form, 'catnom': c.categoria.nombre, 'modnom':modnom})

@login_required
def eliminarprecios(request, pk):
    c = get_object_or_404(Precio, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/precios/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('precios_listar'))
    else:
        return render(request, 'productos/precios/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------
@login_required
def agregaralmacen(request):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Almacen()
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/almacenes/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('almacenes_listar'))
    else:
        form = AlmacenForm()
        return render(request, 'productos/almacenes/agregar.html', {'form': form})

@login_required
def listaralmacenes(request):
    lista = Almacen.objects.all().order_by('nombre')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/almacenes/listar.html', { 'almacenes': clase, 'paginator':paginator })

@login_required
def buscaralmacenes(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Almacen.objects.filter(Q(nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'nombre':c.nombre})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editaralmacenes(request, pk):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Almacen.objects.get(id=pk)
                c.nombre = form.cleaned_data['nombre']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
            print(detalle)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/almacenes/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('almacenes_listar'))
    else:
        c = get_object_or_404(Almacen, pk=pk)
        form = AlmacenForm(initial={'nombre':c.nombre})
        return render(request, 'productos/almacenes/editar.html', {'form': form})

@login_required
def eliminaralmacenes(request, pk):
    c = get_object_or_404(Almacen, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/almacenes/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('almacenes_listar'))
    else:
        return render(request, 'productos/almacenes/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------
@login_required
def agregarproducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Producto()
                pk1 = form.cleaned_data['modelo']
                pk2 = form.cleaned_data['categoria']
                pk3 = form.cleaned_data['precio']
                c.categoria = get_object_or_404(Categoria, pk=pk2)
                c.modelo = get_object_or_404(Modelo, pk=pk1)
                c.precio = get_object_or_404(Precio, pk=pk3)
                c.stock_minimo = form.cleaned_data['stock_minimo']
                c.descripcion = form.cleaned_data['descripcion']
                c.save()
                barra = str(1000000 + int(c.id))
                c.barra = calcularean8(barra)
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                print(detalle)
                return render(request, 'productos/productos/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('productos_listar'))
    else:
        form = ProductoForm()
        return render(request, 'productos/productos/agregar.html', {'form': form})

@login_required
def listarproductos(request):
    lista = Producto.objects.all().order_by('categoria')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/productos/listar.html', { 'lista': clase, 'paginator':paginator })

@login_required
def buscarproductos(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Producto.objects.filter(Q(categoria__nombre__contains = texto)| Q(modelo__marca__nombre__contains = texto)| Q(modelo__nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'categoria':c.categoria.nombre, 'marca':c.modelo.marca.nombre ,'modelo':c.modelo.nombre,'barra':c.barra, 'mayor':str(c.precio.mayor), 'punto':str(c.precio.punto), 'cliente':str(c.precio.cliente), 'stock_minimo':c.stock_minimo})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

def buscarproductos2(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Producto.objects.filter(Q(categoria__nombre__contains = texto)| Q(modelo__marca__nombre__contains = texto)| Q(modelo__nombre__contains = texto)| Q(barra__contains = texto))
            lista = []
            for c in clase:
                nom = c.categoria.nombre + "-" + c.modelo.marca.nombre + "-" +  c.modelo.nombre
                item = {}
                item['id'] = c.pk
                item['label'] = nom
                item['value'] = nom
                lista.append(item)
				#lista.append({'pk':c.pk,'categoria':c.categoria.nombre, 'marca':c.modelo.marca.nombre ,'modelo':c.modelo.nombre, 'mayor':str(c.precio.mayor), 'punto':str(c.precio.punto), 'cliente':str(c.precio.cliente), 'stock_minimo':c.stock_minimo})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarproductos(request, pk):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = get_object_or_404(Producto, pk=pk)
                pk2 = form.cleaned_data['categoria']
                pk1 = form.cleaned_data['modelo']
                pk3 = form.cleaned_data['precio']
                c.categoria = get_object_or_404(Categoria, pk=pk2)
                c.modelo = get_object_or_404(Modelo, pk=pk1)
                c.precio = get_object_or_404(Precio, pk=pk3)
                c.stock_minimo = form.cleaned_data['stock_minimo']
                c.descripcion = form.cleaned_data['descripcion']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/productos/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('productos_listar'))
    else:
        c = get_object_or_404(Producto, pk=pk)
        form = ProductoForm(initial={'categoria':c.categoria.pk,'modelo':c.modelo.pk, 'precio':c.precio.pk, 'stock_minimo':c.stock_minimo, 'descripcion':c.descripcion})
        precios = "Mayor:S/." + str(c.precio.mayor) + "--Punto:S/." + str(c.precio.punto) + "--Cliente:S/." + str(c.precio.cliente)
        modnom = c.modelo.marca.nombre + "-" +  c.modelo.nombre
        extras = {'marcanom':c.modelo.marca.nombre, 'catnom': c.categoria.nombre, 'modnom':modnom, 'precios':precios }
        return render(request, 'productos/productos/editar.html', {'form': form, 'extras':extras})

@login_required
def eliminarproductos(request, pk):
    c = get_object_or_404(Producto, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/productos/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('productos_listar'))
    else:
        return render(request, 'productos/productos/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------

def calcularean8(digits):
    a=1
    pares=0
    impares=0
    for d in digits:
        if a % 2  == 0:
            pares += int(d)
        else:
            impares += int(d)
        a=a +1
    impares=impares*3
    suma = pares + impares
    digito = 10-(suma % 10)
    resultado = digits + str(digito)
    return resultado

@login_required
def agregarsku(request):
    if request.method == 'POST':
        form = SkuForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = Sku()
                pk1 = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk1)
                c.imagen = form.cleaned_data['imagen']
                c.genero = form.cleaned_data['genero']
                c.descripcion = form.cleaned_data['descripcion']
                c.save()
                barra = str(1000000 + int(c.id))
                c.barra = calcularean8(barra)
                c.save()
        except Exception as e:
             detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/sku/agregar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('sku_listar'))
    else:
        form = SkuForm()
        return render(request, 'productos/sku/agregar.html', {'form': form})

@login_required
def listarsku(request):
    lista = Sku.objects.all().order_by('producto')
    page = request.GET.get('page')
    paginator = Paginator(lista, 10)
    try:
        clase = paginator.page(page)
    except PageNotAnInteger:
        clase = paginator.page(1)
    except EmptyPage:
        clase = paginator.page(1)
    return render(request, 'productos/sku/listar.html', { 'lista': clase, 'paginator':paginator })

@login_required
def buscarsku(request):
    if request.is_ajax():
        texto = request.GET['term']
        if texto is not None:
            clase = Sku.objects.filter(Q(barra__contains = texto)|Q(producto__categoria__nombre__contains = texto)| Q(producto__modelo__marca__nombre__contains = texto)| Q(producto__modelo__nombre__contains = texto))
            lista = []
            for c in clase:
				lista.append({'pk':c.pk,'categoria':c.producto.categoria.nombre, 'marca':c.producto.modelo.marca.nombre ,'modelo':c.producto.modelo.nombre, 'barra':str(c.barra), 'imagen':str(c.imagen), 'descripcion':str(c.descripcion), 'genero':c.genero})
            data = json.dumps(lista)
            return HttpResponse(data, content_type='application/json')

@login_required
def editarsku(request, pk):
    if request.method == 'POST':
        form = SkuForm(request.POST)
        detalle = 0
        try:
            if form.is_valid():
                c = get_object_or_404(Sku, pk=pk)
                pk1 = form.cleaned_data['producto']
                c.producto = get_object_or_404(Producto, pk=pk1)
                c.imagen = form.cleaned_data['imagen']
                c.genero = form.cleaned_data['genero']
                c.descripcion = form.cleaned_data['descripcion']
                c.save()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0 or form.is_valid() == False:
                return render(request, 'productos/sku/editar.html', {'form': form, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('sku_listar'))
    else:
        c = get_object_or_404(Sku, pk=pk)
        form = SkuForm(initial={'producto':c.producto.pk,'imagen':c.imagen, 'genero':c.genero, 'descripcion':c.descripcion})
        modnom = c.producto.categoria.nombre + "-" + c.producto.modelo.marca.nombre + "-" +  c.producto.modelo.nombre
        extras = { 'modnom':modnom }
        return render(request, 'productos/sku/editar.html', {'form': form, 'extras':extras})

@login_required
def eliminarsku(request, pk):
    c = get_object_or_404(Sku, pk=pk)
    detalle = 0
    if request.method == 'POST':
        try:
            c.delete()
        except Exception, e:
            detalle = "Error: " + str(e)
        finally:
            if detalle != 0:
                return render(request, 'productos/sku/eliminar.html', {'c': c, 'detalle':detalle})
            else:
                return redirect(reverse_lazy('sku_listar'))
    else:
        return render(request, 'productos/sku/eliminar.html', {'c': c})
#-------------------------------------------------------------------------------
