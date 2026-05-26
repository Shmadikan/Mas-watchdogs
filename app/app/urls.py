"""
URL configuration for app project.

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
from admin_panel import views as admin_views
from auditor_panel import views as auditor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_views.PanelView.as_view(), name='panel'),
    path('/start_connection', admin_views.IpRun.as_view(), name='start_connection'),
    path('analyze_result/', admin_views.AnalyzeResultReceive.as_view(), name='store_report'),
    path('get_report/', admin_views.AnalyzeResultPoll.as_view(), name='poll_report'),
    path('panel/auditor/', auditor_views.IpPoolRead.as_view(), name='auditor'),
    path('panel/auditor/create', auditor_views.IpPoolCreate.as_view(), name='create'),
    path('panel/auditor/<int:id>', auditor_views.IpPoolDetail.as_view(), name='detail'),
    path('panel/auditor/<int:id>/delete', auditor_views.IpPoolDelete.as_view(), name='delete'),
    path('panel/auditor/<int:id>/update', auditor_views.IpPoolUpdate.as_view(), name='update'),
]
