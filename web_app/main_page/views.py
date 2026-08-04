import pdb
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
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
        }
        return render(request, "main_page.html", context=context)

class ScanResultView(View):
    def get(self, request, *args, **kwargs):
        scan_result = ScanResult.objects.all()
        transform_data = list(map(lambda x: {
            'id': x.pk,
            'date': x.date.strftime('%Y.%m.%d %H:%M'),
            'title': x.title,
            'desc': x.description
        }, scan_result))
        response = JsonResponse(transform_data, safe=False)
        return response



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


class IpPageAgentConnect(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        result = json.loads(request.body)
        try:
            ScanResult.handle_ip(result)
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
