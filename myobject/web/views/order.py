from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from myadmin.models import Orders, Payment, OrderDetail, User
import datetime


class ShowOrder(View):
    def get(self, request, pIndex=1):
        ''' 浏览订单信息 '''
        umod = Orders.objects
        sid = request.session['shop_name']['id']  # 获取当前店铺id号
        user_id = request.session.get('web_user')['id']
        ulist = umod.filter(shop_id=sid, user_id=user_id)
        mywhere = []
        # 获取、判断并封装状态status搜索条件
        status = request.GET.get('status', '')
        if status != '':
            ulist = ulist.filter(status=status)
            mywhere.append("status=" + status)

        ulist = ulist.order_by("id")  # 对id排序
        # 执行分页处理
        pIndex = int(pIndex)
        page = Paginator(ulist, 10)  # 以每页10条数据分页
        maxpages = page.num_pages  # 获取最大页数
        # 判断当前页是否越界
        if pIndex > maxpages:
            pIndex = maxpages
        if pIndex < 1:
            pIndex = 1
        list2 = page.page(pIndex)  # 获取当前页数据
        plist = page.page_range  # 获取页码列表信息

        context = {"orderslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
        return render(request, "web/list.html", context)

    def post(self, request, pIndex):
        try:
            od = Orders()
            od.shop_id = request.session['shop_name']['id']
            od.member_id = 0
            od.user_id = request.session['web_user']['id']
            od.money = request.session['total_mo']
            od.status = 1
            od.payment_status = 1
            od.create_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            od.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            od.save()

            op = Payment()
            op.order_id = od.id
            op.member_id = 0
            op.money = request.session['total_mo']
            op.type = 2
            op.bank = request.POST.get('bank', 2)
            op.status = 2
            op.create_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            op.update_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            op.save()

            # 执行订单详情的添加
            cartlist = request.session.get("cartlist", {})  # 获取购物车中的菜品信息
            # 遍历购物车中的菜品并添加到订单详情中
            for item in cartlist.values():
                ov = OrderDetail()
                ov.order_id = od.id  # 订单id
                ov.product_id = item['id']  # 菜品id
                ov.product_name = item['name']  # 菜品名称
                ov.price = item['price']  # 单价
                ov.quantity = item['num']  # 数量
                ov.status = 1  # 状态:1正常/9删除
                ov.save()

            del request.session["cartlist"]
            del request.session['total_mo']
            return HttpResponse("Y")
        except Exception as e:
            print(e)
            return HttpResponse('N')


def DelOrder(request):
    pass


def DetailOrder(request):
    pass