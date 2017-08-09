from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^personas/agregar$', agregarpersona, name='personas_agregar'),
    url(r'^personas/listar$', listarpersonas, name='personas_listar'),
    url(r'^personas/buscar-ajax$', buscarpersonas, name='personas_buscar_ajax'),
    url(r'^personas/editar/(?P<pk>[0-9]+)/$', editarpersona, name='personas_editar'),
    url(r'^personas/eliminar/(?P<pk>[0-9]+)/$', eliminarpersona, name='personas_eliminar'),
    ]
