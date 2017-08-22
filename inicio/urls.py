from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.views.generic  import TemplateView
from . import views
from .views import *
urlpatterns = [
    url(r'^$', login, {'template_name': 'inicio/index.html'}, name='home'),
    url(r'^principal$', principal.as_view(), name='principal'),
    url(r'^salir/$', logout_then_login, name='salir'),
    url(r'^comisiones/agregar$', agregarcomision, name='agregarcomision'),
    url(r'^comisiones/listar$', listarcomisiones, name='comisiones_listar'),
    #url(r'^comisiones/buscar-ajax$', buscarventas, name='ventas_buscar_ajax'),
    #url(r'^comisiones/editar/(?P<pk>[0-9]+)/$', editarcomision, name='comisiones_editar'),
    #url(r'^comisiones/eliminar/(?P<pk>[0-9]+)/$', eliminarcomision, name='comisiones_eliminar'),
    ]
