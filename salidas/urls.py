from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^perdidas/agregar$', agregarperdida, name='agregarperdida'),
    #url(r'^ventas/agregar-ajax$', agregarventa2, name='ventas_agregar'),
    url(r'^perdidas/listar$', listarperdidas, name='perdidas_listar'),
    #url(r'^ventas/buscar-ajax$', buscarventas, name='ventas_buscar_ajax'),
    #url(r'^ventas/editar/(?P<pk>[0-9]+)/$', editarventa, name='ventas_editar'),
    #url(r'^ventas/eliminar/(?P<pk>[0-9]+)/$', eliminarventa, name='ventas_eliminar'),
    ]
