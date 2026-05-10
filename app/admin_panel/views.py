from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
# Create your views here.
from auditor_panel import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import IpSerializer

class PanelView(ListView):
    model = models.IpPool
    template_name = 'panel.html'
    context_object_name = 'ip_pools'


class IpRun(APIView):
    def post(self, request, *args, **kwargs):
        Serializer = IpSerializer(data=request.data)
        if Serializer.is_valid():
           print(Serializer.data)
           return Response(Serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)




