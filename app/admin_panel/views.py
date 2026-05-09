from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
# Create your views here.


class panelView(TemplateView):
    template_name = 'panel.html'


