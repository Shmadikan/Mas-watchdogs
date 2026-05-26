from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from auditor_panel import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import IpSerializer
import redis
import json


def netmask_to_cidr(mask_ip: str) -> int:
    parts = mask_ip.split('.')
    binary = ''.join(f'{int(p):08b}' for p in parts)
    return binary.count('1')


analysis_reports = []


class PanelView(ListView):
    model = models.IpPool
    template_name = 'panel.html'
    context_object_name = 'ip_pools'


class IpRun(APIView):
    def post(self, request, *args, **kwargs):
        Serializer = IpSerializer(data=request.data)
        if Serializer.is_valid():
            pool_data = Serializer.data
            subnet = f"{pool_data['ip']}/{netmask_to_cidr(pool_data['mask'])}"

            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.publish("externalReceive", json.dumps([subnet]))

            return Response(
                {"status": "started"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyzeResultReceive(APIView):
    def post(self, request, *args, **kwargs):
        report = request.data
        analysis_reports.append(report)
        return Response({"status": "stored"}, status=status.HTTP_200_OK)


class AnalyzeResultPoll(APIView):
    def get(self, request, *args, **kwargs):
        if analysis_reports:
            return Response({"report": analysis_reports[-1]}, status=status.HTTP_200_OK)
        return Response({"status": "not_found"}, status=status.HTTP_404_NOT_FOUND)




