"""LeaveRequestApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^employee/(?P<pk>\d+)$', Home.as_view(), name='home'),
    #url(r'^(?P<pk>\d+)/$', TeamDetails.as_view(), name='team-details'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^apply-leave/$', ApplyLeave.as_view(), name='apply-leave'),
    url(r'^super-admin/$', SuperAdmin.as_view(), name='super-admin'),
    url(r'^save-leave-status/(?P<pk>\d+)/$', SaveLeaveStatus.as_view(), name='save leave status'),
    url(r'^delete-leave-application/(?P<pk>\d+)/$', DeleteLeaveApplication.as_view(), name='delete leave application'),

    
    
]
