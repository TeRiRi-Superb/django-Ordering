#前台大堂点餐端子路由文件
from django.urls import path, include
from web.views.index import IndexView, LoginView, logout, verify
from web.views.cart import addcart, changecart, clearcart, delcart

urlpatterns = [
    path('login/', LoginView.as_view(), name="web_login"),
    path('logout/', logout, name='web_logout'),
    path('verify/', verify, name='web_verify'),

    path('web/', include([
        path('', IndexView.as_view(), name="web_index"),
        path('cart/add/<str:pid>', addcart, name='addcart'),
        path('cart/change/', changecart, name='changecart'),
        path('cart/clear/', clearcart, name='clearcart'),
        path('cart/del/<str:pid>', delcart, name='delcart'),
    ])),
]
