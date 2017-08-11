from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class principal(LoginRequiredMixin, TemplateView):
    template_name = "inicio/base.html"
