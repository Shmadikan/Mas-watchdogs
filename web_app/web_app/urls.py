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
from django.urls import path
from main_page import views as m_views
from profiles import views as p_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('control/', m_views.ControlPage.as_view(), name = "control_page"),
    path('control/ip/update/<int:pk>/', m_views.IpPageUpdate.as_view(), name = "ip"),
    path('control/ip/create', m_views.IpPageCreate.as_view(), name = "ip_create"),
    path('control/ip/delete/<int:pk>/', m_views.IpPageDelete.as_view(), name = "ip_delete"),
    path('control/send', m_views.IpPageAgentConnect.as_view(), name='ip_send'),
    path('control/results', m_views.ScanResultView.as_view(), name='ip_scan_results'),
    path('control/results/get/', m_views.ScanResultObjectView.as_view(), name='ip_scan_get'),
    path('control/results/<int:pk>/', m_views.ScanResultDetailView.as_view(), name='ip_scan_detail'),
    path('control/results/delete', m_views.ScanResultDelete.as_view(), name='ip_scan_delete'),
    path('control/polling', m_views.IpPageAgentPooling.as_view(), name='ip_polling'),
    path('profiles/', p_views.ProfilesView.as_view(), name = 'profiles_view'),
    path('profiles/registrate/', p_views.ProfileCreate.as_view(), name = 'profile_create'),
    path('profiles/settings', p_views.Profile.as_view(), name='profile_setting'),
    path('profiles/system', p_views.ProfileSystemSetting.as_view(), name='system_settings'),
    path('', p_views.RedirectFromStart.as_view(), name='start'),
]
