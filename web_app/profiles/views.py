import json

import pdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, CreateView, RedirectView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy

from .apps import ProfilesConfig
from .models import UserSetting


# Create your views here.
class ProfilesView(View):

    def get(self, request, *arg, **kwargs):
        context = {
            "users" : User.objects.values_list('username', flat=True)
        }
        return render(request, 'registration/profiles_view.html', context=context)
    def post(self, request: HttpRequest, *arg, **kwargs):
        try:
            user = User.objects.get_by_natural_key(request.POST.get('username'))
            login(request, user)
            user_setting = user.setting
            response = HttpResponseRedirect(reverse_lazy('control_page'), status=302)
            response.set_cookie('language', user_setting.language)
            response.set_cookie('theme', user_setting.site_theme)
            response.set_cookie('pooling', user_setting.pooling_interval)
            return response
        except Exception as e:
            return HttpResponse(status=500)

class ProfileCreate(CreateView):
    model = User
    fields = ['username']
    template_name = 'registration/profile_create.html'
    success_url = reverse_lazy('profiles_view')

    def form_valid(self, form):
        response = super().form_valid(form)
        UserSetting(language='eng', site_theme='default', pooling_interval=2, user=form.instance).save()
        return response


class RedirectFromStart(RedirectView):
    url = reverse_lazy('profiles_view')

class Profile(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, template_name='registration/profile_settings.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            user = User.objects.get(id=request.session['_auth_user_id'])
            user_language = request.POST.get('language')
            user_theme = request.POST.get('color')
            pooling = request.POST.get('pooling')
            user_setting = user.setting
            user_setting.language = user_language
            user_setting.site_theme = user_theme
            user_setting.pooling_interval = int(pooling)
            user_setting.save()


            response = HttpResponseRedirect(reverse_lazy('control_page'), status=302)
            response.set_cookie('language', user_language)
            response.set_cookie('theme', user_theme)
            response.set_cookie('pooling', pooling)
            return response
        except Exception as e:
            return HttpResponse(status=500)


class ProfileSystemSetting(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, template_name='registration/system_settings.html')

    def post(self, request: HttpRequest, *args, **kwargs):
        api_key = request.POST.get('api-key')
        url = request.POST.get('model-url')
        model = request.POST.get('model')
        data = json.dumps({
            'api-key': api_key,
            'model-url': url,
            'model': model
        })
        ProfilesConfig.redis_client.publish('webapp-coordinator', data)
        return HttpResponseRedirect(reverse_lazy('control_page'), status=302)


