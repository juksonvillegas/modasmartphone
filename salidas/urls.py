from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^perdidas/agregar$', agregarperdida, name='agregarperdida'),
    url(r'^perdidas/listar$', listarperdidas, name='perdidas_listar'),
    #url(r'^ventas/buscar-ajax$', buscarventas, name='ventas_buscar_ajax'),
    url(r'^perdidas/editar/(?P<pk>[0-9]+)/$', editarperdida, name='perdidas_editar'),
    url(r'^perdidas/eliminar/(?P<pk>[0-9]+)/$', eliminarperdida, name='perdidas_eliminar'),
    url(r'^gastos/agregar$', agregargasto, name='agregargasto'),
    url(r'^gastos/listar$', listargastos, name='gastos_listar'),
    #url(r'^gastos/buscar-ajax$', buscarventas, name='ventas_buscar_ajax'),
    url(r'^gastos/editar/(?P<pk>[0-9]+)/$', editargasto, name='gastos_editar'),
    url(r'^gastos/eliminar/(?P<pk>[0-9]+)/$', eliminargasto, name='gastos_eliminar'),
    ]
