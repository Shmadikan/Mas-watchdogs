from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class IpPoolRead(ListView):
    model = IpPool
    paginate_by = 20
    context_object_name = 'ip_pools'


class IpPoolCreate(CreateView):
    model = IpPool
    fields = ['ip', 'description', 'ports', "mask"]
    success_url = reverse_lazy("auditor")


class IpPoolDetail(DetailView):
    model = IpPool
    pk_url_kwarg = 'id'




class IpPoolDelete(DeleteView):
    model = IpPool
    success_url = reverse_lazy("auditor")
