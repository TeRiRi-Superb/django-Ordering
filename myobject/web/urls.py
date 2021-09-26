#前台大堂点餐端子路由文件
from django.urls import path,include
from web.views.index import IndexView, LoginView, logout, verify

urlpatterns = [
    path('web/', IndexView.as_view(), name="web_index"),
    path('login/', LoginView.as_view(), name="web_login"),
    path('logout/', logout, name='web_logout'),
    path('verify/', verify, name='web_verify'),
]
