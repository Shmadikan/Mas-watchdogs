from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class auditorView(ListView):
    model = IpPool
    paginate_by = 20
    context_object_name = 'ip_pools'
