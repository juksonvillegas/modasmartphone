from django.conf.urls import include, url
from django.contrib.auth.views import login, logout_then_login
from django.views.generic  import TemplateView
from . import views
from .views import *
urlpatterns = [
    url(r'^$', login, {'template_name': 'inicio/index.html'}, name='home'),
    url(r'^consignaciones/agregar$', consignaciones_agregar.as_view(), name='principal'),
    url(r'^salir/$', logout_then_login, name='salir'),
    ]
