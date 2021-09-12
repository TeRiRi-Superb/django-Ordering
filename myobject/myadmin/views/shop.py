from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from myadmin.models import Shop
from django.db.models import Q
from django.core.paginator import Paginator
import datetime


class ShopView(View):
    def get(self, request, page=1):
        shops = Shop.objects.all()
        where = []

        table_search = request.GET.get('table_search')

        if table_search:
            shops = Shop.objects.filter(Q(name__contains=table_search) | Q(address__contains=table_search))
            where.append('table_search=' + table_search)  # 储存搜索信息 在跳转页面时保持搜索

        paginator = Paginator(shops, 5)
        page = int(page)
        maxindex = paginator.num_pages  # 获取最大列表数

        if page > maxindex:
            page = maxindex
        if page < 1:
            page = 1

        pagecontext = paginator.page(page)  # 当前页数据
        prange = paginator.page_range  # 获取分页页码列表

        context = {
            'shops': pagecontext,
            'where': where,
            'prange': prange,  #所有页页码
            'maxindex': maxindex,  # 最大页码
            'page': page,  # 当前页
        }
        return render(request, 'myadmin/index/shop.html', context)


class AddShop(View):
    def get(self, request):
        return render(request, 'myadmin/index/addshop.html')

    def post(self, request):
        shopname = request.POST.get('shopname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        shop_img = request.POST.get('shop_img')
        shop_logo = request.POST.get('shop_logo')
        try:
            add_shop = Shop()
            add_shop.name = shopname
            add_shop.cover_pic = shop_img
            add_shop.banner_pic = shop_logo
            add_shop.address = address
            add_shop.phone = phone
            add_shop.status = 1
            add_shop.create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_shop.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_shop.save()

            context = {
                'info': '添加成功',
            }
        except Exception as e:
            context = {
                'info': '添加失败',
            }

        return render(request, 'myadmin/user/info.html', context)


class DelShop(View):
    def get(self, request, shopid):
        try:
            del_shop = Shop.objects.get(id=shopid)
            del_shop.delete()
            context = {
                'info': '删除成功'
            }
        except Exception as e:
            context = {
                'info': '删除失败'
            }

        return render(request, 'myadmin/user/info.html', context)


class UpdateShop(View):
    def get(self, request, shopid):
        try:
            sid = Shop.objects.get(id=shopid)
            context = {
                'sid': sid
            }
            return render(request, 'myadmin/index/updateshop.html', context)
        except Exception as e:
            context = {'info': '修改信息错误'}
            print(e)
            return render(request, 'myadmin/user/info.html', context)

    def post(self, request, shopid):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        shop_img = request.POST.get('shop_img')
        shop_logo = request.POST.get('shop_logo')
        status = request.POST.get('status')

        try:
            shops = Shop.objects.get(id=shopid)
            shops.name = name
            shops.phone = phone
            shops.status = status
            shops.address = address
            shops.cover_pic = shop_img
            shops.banner_pic = shop_logo
            shops.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            shops.save()

            context = {'info': '修改成功'}
        except Exception as e:
            context = {'info': '修改失败'}

        return render(request, 'myadmin/user/info.html', context)


