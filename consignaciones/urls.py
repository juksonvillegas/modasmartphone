from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^consignaciones/agregar$', agregarconsignacion, name='consignaciones_agregar'),
    url(r'^consignaciones/listar$', listarconsignaciones, name='consignaciones_listar'),
    url(r'^consignaciones/agregar-ajax$', agregarconsignacion2, name='consignaciones_agregar'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/$', editarconsignaciones, name='consignaciones_editar'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/observacion$', editarconsignacionesobservacion, name='consignaciones_editar'),
    ]
