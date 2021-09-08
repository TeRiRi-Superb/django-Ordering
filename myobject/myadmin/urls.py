"""myobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from myadmin.views.index import indexView
from myadmin.views.user import VIPadmin, AddVIP, DelVIP, EditVIP

urlpatterns = [
    re_path(r'^index$', indexView.as_view(), name='index'),
    re_path(r'^VIP(?P<page>.*)$', VIPadmin.as_view(), name='VIP'),
    re_path(r'^adduser$', AddVIP.as_view(), name='adduser'),
    re_path(r'^deluser(?P<userid>.*)$', DelVIP.as_view(), name='deluser'),
    re_path(r'^edituser(?P<userid>.*)$', EditVIP.as_view(), name='edituser'),
]
