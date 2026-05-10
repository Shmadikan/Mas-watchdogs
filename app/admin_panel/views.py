from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
# Create your views here.
from auditor_panel import models



class panelView(ListView):
    model = models.IpPool
    template_name = 'panel.html'
    context_object_name = 'ip_pools'


