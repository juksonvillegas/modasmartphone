from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^consignaciones/agregar$', agregarconsignacion, name='consignaciones_agregar'),
    url(r'^consignaciones/listar$', listarconsignaciones, name='consignaciones_listar'),
    url(r'^consignaciones/reportes$', listarconsignacionestodas, name='consignaciones_listar_todas'),
    url(r'^consignaciones/agregar-ajax$', agregarconsignacion2, name='consignaciones_agregar'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/$', editarconsignaciones, name='consignaciones_editar_datos'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/observacion$', editarconsignacionesobservacion, name='consignaciones_editar_observacion'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/pagado$', editarconsignacionespagado, name='consignaciones_editar_pagado'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/devuelto$', editarconsignacionesdevuelto, name='consignaciones_editar_devuelto'),
    url(r'^consignaciones/editar/(?P<pk>[0-9]+)/pagoydevolvio$', editarconsignacionespagoydevolvio, name='consignaciones_editar_pagoydevolvio'),
    url(r'^consignaciones/eliminar/(?P<pk>[0-9]+)/$', eliminarconsignacion, name='consignaciones_eliminar'),
    ]
