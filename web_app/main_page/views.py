from functools import reduce
from django.db.models import Q

import pdb
import json

from django.db.models.lookups import LessThan
from redis.client import PubSub
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .apps import MainPageConfig
from django.views.generic import View, UpdateView, CreateView, DeleteView, DetailView

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
        transform_data = ScanResult.all_formating()
        response = JsonResponse(transform_data, safe=False)
        return response

class ScanResultObjectView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            pdb.set_trace()
            id = request.GET.get('id')
            response = JsonResponse(ScanResult.get_format(id=id), status=200)
            return response
        except Exception:
            return HttpResponse(status=503)

class ScanResultDelete(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            id_delete = json.loads(request.body)
            print(id_delete)
            result = ScanResult.objects.all().filter(id__in=id_delete['delete_ids'])
            result.delete()
            return HttpResponse(status=200)
        except Exception as e:

            print(e)
            return HttpResponse(status=500)


class ScanResultDetailView(DetailView):
    model = ScanResult
    template_name = 'scan_detail.html'




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
        redis_client: redis.Redis = MainPageConfig.redis_client
        results:list[dict[str, str]] = json.loads(request.body)
        try:
            ip_list = []
            for result in zip(ScanResult.handle_ip(results), results):
                ip = result[1]['ip']
                subnet = result[1]['subnet']
                id_result = result[0].id
                message = (IpTable.ipv4_transform(ip, subnet), id_result)
                ip_list.append(message)
            redis_client.publish('externalReceive', json.dumps(ip_list))
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

class IpPageAgentPooling(View):
    redis_client: redis.client.Redis = MainPageConfig.redis_client
    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            message = MainPageConfig.pubsub.get_message()
            if message:
               if message['type'] == 'message':
                  data: dict = json.loads(message['data'])
                  id = data['id']
                  report = data['report']
                  scan_result = ScanResult.objects.get(id=id)
                  scan_result.title = 'result 1'
                  scan_result.description = report
                  scan_result.save()
                  return JsonResponse({'result_id_change': id}, status=200)
            else:
               return HttpResponse(status=204)
        except:
            return HttpResponse(status=500)