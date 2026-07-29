import pdb

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DetailView, UpdateView, CreateView, DeleteView

from .models import IpTable, ScanResult
# Create your views here.

class ControlPage(View):
    def get(self, request, *args, **kwargs):
        context = {
        "ips": IpTable.objects.all(),
        "results": ScanResult.objects.all()
        }
        return render(request, "main_page.html", context=context)

class IpCrudMixin:
    model = IpTable
    fields = ['ip', 'subnet']
    success_url = reverse_lazy('control_page')


class IpPageUpdate(IpCrudMixin, UpdateView):
    template_name = 'ip_page_form.html'



class IpPageCreate(IpCrudMixin, CreateView):
    template_name = 'ip_page_form.html'


class IpPageDelete(IpCrudMixin, DeleteView):
    pass
