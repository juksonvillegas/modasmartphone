from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.views.generic  import TemplateView
from . import views
from .views import *
urlpatterns = [
    url(r'^desbloqueos/agregar$', agregardesbloqueo, name='agregardesbloqueo'),
    url(r'^desbloqueos/listar$', listardesbloqueos, name='desbloqueos_listar'),
    url(r'^desbloqueos/entregar/(?P<pk>[0-9]+)/$', entregardesbloqueo, name='desbloqueos_entregar'),
    #url(r'^comisiones/ranking$', rankingcomisiones, name='ranking_listar'),
    #url(r'^comisiones/buscar-ajax$', buscarventas, name='ventas_buscar_ajax'),
    #url(r'^comisiones/editar/(?P<pk>[0-9]+)/$', editarcomision, name='comisiones_editar'),
    #url(r'^comisiones/eliminar/(?P<pk>[0-9]+)/$', eliminarcomision, name='comisiones_eliminar'),
    #url(r'^caja/listar$', listarcajas, name='caja_listar'),
    #url(r'^comisiones/reportes$', reportecomisiones, name='reporte_comisiones'),
    #url(r'^comisiones/reportepersona$', reportecomsionpersona, name='reportecomisionpersona'),
    ]
