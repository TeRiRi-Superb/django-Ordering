#前台大堂点餐端子路由文件
from django.urls import path, include
from web.views.index import IndexView, LoginView, logout, verify
from web.views.cart import addcart, changecart, clearcart, delcart
from web.views.order import ShowOrder, DetailOrder, DelOrder

urlpatterns = [
    path('login/', LoginView.as_view(), name="web_login"),
    path('logout/', logout, name='web_logout'),
    path('verify/', verify, name='web_verify'),

    path('web/', include([
        path('', IndexView.as_view(), name="web_index"),
        path('cart/add/<str:pid>', addcart, name='addcart'),
        path('cart/change/<str:pid>', changecart, name='changecart'),
        path('cart/clear/', clearcart, name='clearcart'),
        path('cart/del/<str:pid>', delcart, name='delcart'),
        path('order/show<str:pIndex>', ShowOrder.as_view(), name='showorder'),
        path('order/Del', DelOrder, name='delorder'),
        path('order/Detail', DetailOrder, name='detailorder'),
    ])),
]
