from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class indexView(View):
    def get(self, request):
        return render(request, 'myadmin/index/admin.html')


class login_User(View):
    '''登录'''
    def get(self, request):
        return render(request, 'myadmin/index/login.html')