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
from myadmin.views.index import indexView, login_User, logout_User, verify
from myadmin.views.user import VIPadmin, AddVIP, DelVIP, EditVIP
from myadmin.views.shop import ShopView, AddShop, DelShop, UpdateShop
from myadmin.views.category import CateGoryView, DelCategory, EditCategory, AddCategory
from myadmin.views.variety import VarietyView, AddVariety, DelVariety, EditVariety

urlpatterns = [
    path('login/', login_User.as_view(), name='login'),
    path('logout/', logout_User.as_view(), name='logout'),
    path('verify/', verify, name='verify'),

    re_path(r'^shop(?P<page>.*)$', ShopView.as_view(), name='shop'),
    path('addshop/', AddShop.as_view(), name='addshop'),
    re_path(r'^delshop(?P<shopid>.*)$', DelShop.as_view(), name='delshop'),
    re_path(r'^updateshop(?P<shopid>.*)$', UpdateShop.as_view(), name='updateshop'),

    re_path(r'^category(?P<page>.*)$', CateGoryView.as_view(), name='category'),
    re_path(r'^delcate(?P<cate_id>.*)$', DelCategory.as_view(), name='delcate'),
    re_path(r'^editcate(?P<cate_id>.*)$', EditCategory.as_view(), name='editcate'),
    path('addcate/', AddCategory.as_view(), name='addcate'),

    re_path(r'^variety(?P<page>.*)$', VarietyView.as_view(), name='variety'),
    path('addvariety/', AddVariety.as_view(), name='addvariety'),
    re_path(r'^delvariety(?P<variety_id>.*)$', DelVariety.as_view(), name='delvariety'),
    re_path(r'^editvariety(?P<product_id>.*)$', EditVariety.as_view(), name='editvariety'),

    re_path(r'^index$', indexView.as_view(), name='index'),
    re_path(r'^VIP(?P<page>.*)$', VIPadmin.as_view(), name='VIP'),
    re_path(r'^adduser$', AddVIP.as_view(), name='adduser'),
    re_path(r'^deluser(?P<userid>.*)$', DelVIP.as_view(), name='deluser'),
    re_path(r'^edituser(?P<userid>.*)$', EditVIP.as_view(), name='edituser'),
]
