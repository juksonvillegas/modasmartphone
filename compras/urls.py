from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^compras/agregar$', agregarcompra, name='compras_agregar'),
    url(r'^compras/agregar-ajax$', agregarcompra2, name='compras_agregar'),
    url(r'^compras/listar$', listarcompras, name='compras_listar'),
    url(r'^compras/buscar-ajax$', buscarcompras, name='compras_buscar_ajax'),
    url(r'^compras/editar/(?P<pk>[0-9]+)/$', editarcompra, name='compras_editar'),
    url(r'^compras/eliminar/(?P<pk>[0-9]+)/$', eliminarcompra, name='compras_eliminar'),
    ]
