from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework import serializers


class IpPoolBaseView:
    model = IpPool
    fields = ['ip', 'description', 'ports', 'mask']
    success_url = reverse_lazy("auditor")



class IpPoolRead(ListView):
    model = IpPool
    paginate_by = 20
    context_object_name = 'ip_pools'


class IpPoolCreate(IpPoolBaseView, CreateView):
    pass


class IpPoolDetail(DetailView):
    model = IpPool
    pk_url_kwarg = 'id'


class IpPoolUpdate(IpPoolBaseView, UpdateView):
    pk_url_kwarg = 'id'


class IpPoolDelete(DeleteView):
    model = IpPool
    pk_url_kwarg = 'id'
    success_url = reverse_lazy("auditor")

