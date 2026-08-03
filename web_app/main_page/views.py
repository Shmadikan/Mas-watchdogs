import pdb

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DetailView, UpdateView, CreateView, DeleteView

from .models import IpTable, ScanResult
# Create your views here.

class ControlPage(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request, *args, **kwargs):
        user_id = self.request.session.get('_auth_user_id')
        context = {
            "ips": IpTable.objects.all().filter(user_id_id=user_id),
            "results": ScanResult.objects.all()
        }
        return render(request, "main_page.html", context=context)


class IpCrudMixin(LoginRequiredMixin):
    raise_exception = True
    model = IpTable
    fields = ['ip', 'subnet']
    success_url = reverse_lazy('control_page')


class IpPageUpdate(IpCrudMixin, UpdateView):
    template_name = 'ip_page_form.html'


class IpPageCreate(IpCrudMixin, CreateView):
    template_name = 'ip_page_form.html'
    def form_valid(self, form):
        model = form.instance
        model.user_id_id = self.request.session.get('_auth_user_id')
        return super().form_valid(form)


class IpPageDelete(IpCrudMixin, DeleteView):
    pass
