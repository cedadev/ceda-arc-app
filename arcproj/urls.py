"""arcproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

import arcapp.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jobs/', arcapp.views.view_jobs, name='jobs'),
    url(r'^job/([0-9]+)/', arcapp.views.view_job, name='job'),
    url(r'^submit/', arcapp.views.view_submit, name='submit'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', arcapp.views.view_logout, name='logout'),
    url(r'^download/([0-9]+)/', arcapp.views.download, name='download'),
    url(r'^.*', arcapp.views.view_home, name='home')
]
