from django.shortcuts import reverse, redirect
import re


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path

        pathlist = [reverse('myadmin:login'), reverse('myadmin:logout'), reverse('myadmin:verify')]

        if re.match(r'^/myadmin', path) and (path not in pathlist):
            # 通过session判断是否登录
            if 'login_user' not in request.session:
                return redirect(reverse('myadmin:login'))

        if re.match(r'^/web', path):
            # 通过session判断是否登录
            if 'web_user' not in request.session:
                return redirect(reverse('web:web_login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response