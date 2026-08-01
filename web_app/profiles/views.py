import pdb

from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse
from django.forms import Form

# Create your views here.
class ProfilesView(View):

    def get(self, request, *arg, **kwargs):
        context = {
            "users" : User.objects.values_list('username', flat=True)
        }
        return render(request, 'registration/profiles_view.html', context=context)
    def post(self, request: HttpRequest, *arg, **kwargs):
        user = User.objects.get_by_natural_key(request.POST.get('username'))
        try:
            login(request, user)
            response = HttpResponseRedirect('http://127.0.0.1:8188/control/', status=302)
            response.set_cookie('language','rus', httponly=True)
            response.set_cookie('theme', 'white', httponly=True)
            return response
        except:
            return HttpResponse(status=500)

class ProfileCreate(CreateView):
    model = User
    fields = ['username']
    template_name = 'registration/profile_create.html'
    success_url = reverse_lazy('profiles_view')


