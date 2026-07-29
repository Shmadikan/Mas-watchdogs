import pdb

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DetailView, UpdateView, CreateView

from .models import IpTable, ScanResult
# Create your views here.

class ControlPage(View):
    def get(self, request, *args, **kwargs):
        context = {
        "ips": IpTable.objects.all(),
        "results": ScanResult.objects.all()
        }
        return render(request, "main_page.html", context=context)


class IpPageUpdate(UpdateView):
    model = IpTable
    fields = ['ip', 'subnet']
    template_name = 'ip_page_update.html'
    success_url = reverse_lazy('control_page')

class IpPageCreate(CreateView, IpPageUpdate):
    template_name = 'ip_page_create.html'
