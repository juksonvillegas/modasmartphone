from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^consignaciones/agregar$', agregarconsignacion, name='consignaciones_agregar'),
    url(r'^consignaciones/listar$', listarconsignaciones, name='consignaciones_listar'),
    ]
