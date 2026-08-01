"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main_page import views as m_views
from profiles import views as p_views
from django.contrib.auth.views import LoginView

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('control/', m_views.ControlPage.as_view(), name = "control_page"),
    path('control/ip/update/<int:pk>/', m_views.IpPageUpdate.as_view(), name = "ip"),
    path('control/ip/create', m_views.IpPageCreate.as_view(), name = "ip_create"),
    path('control/ip/delete/<int:pk>/', m_views.IpPageDelete.as_view(), name = "ip_delete"),
    path('profiles/', p_views.ProfilesView.as_view(), name = 'profiles_view'),
    path('profiles/registrate/', p_views.ProfileCreate.as_view(), name = 'profile_create'),
    path('profiles/login', p_views.ProfileLogin.as_view(), name='profile_login'),
    path('__debug__/', include(debug_toolbar.urls))
]
