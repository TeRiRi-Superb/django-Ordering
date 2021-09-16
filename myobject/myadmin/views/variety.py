# 菜品信息
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from myadmin.models import Shop, Category, Product
import datetime
import time


class VarietyView(View):
    def get(self, request, page):
        products = Product.objects.all().order_by('id')
        mywhere = []

        table_search = request.GET.get('table_search')

        if table_search:
            products = Product.objects.filter(name__contains=table_search)
            mywhere.append('table_search=' + table_search)

        for product in products:
            shop_id = product.shop_id
            category_id = product.category_id

            product.shop_name = Shop.objects.get(id=shop_id).name
            product.category_name = Category.objects.get(id=category_id).name

        paginator = Paginator(products, 10)
        page = int(page)
        maxindex = paginator.num_pages

        if page > maxindex:
            page = maxindex
        if page < 1:
            page = 1

        pagecontext = paginator.page(page)  # 指定分页信息
        pagerange = paginator.page_range  # 分页列表

        context = {
            'products': pagecontext,
            'pagerange': pagerange,
            'maxindex': maxindex,
            'page': page,
            'mywhere': mywhere,
        }

        return render(request, 'myadmin/food/variety.html', context)


class AddVariety(View):
    def get(self, request):
        Shops = Shop.objects.all().order_by('id')
        categorys = Category.objects.all().order_by('id')

        context = {
            'shops': Shops,
            'categorys': categorys,
        }
        return render(request, 'myadmin/food/addvariety.html', context)

    def post(self, request):
        shop_id = request.POST.get('shop')
        category_id = request.POST.get('category')
        name = request.POST.get('variety')
        price = request.POST.get('price')
        variety_img = request.FILES.get('variety_img')
        print(variety_img)

        if not all([shop_id, name, category_id, price, variety_img]):
            context = {
                'info': '数据不全'
            }
            return render(request, 'myadmin/user/info.html', context)

        cover_pic = str(time.time()) + '.' + variety_img.name.split('.').pop()
        with open(f'static/uploads/product/{cover_pic}', 'wb+') as f:
            for chunk in variety_img.chunks():
                f.write(chunk)

        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        Product.objects.create(shop_id=shop_id, category_id=category_id, cover_pic=cover_pic, name=name, price=price, status=1, create_at=create_time, update_at=create_time)

        context = {
            'info': '添加成功'
        }

        return render(request, 'myadmin/user/info.html', context)


class DelVariety(View):
    def get(self, request, variety_id):
        try:
            del_product = Product.objects.get(id=variety_id)
            del_product.delete()

            context = {
                'info': '删除成功'
            }

            return render(request, 'myadmin/user/info.html', context)
        except Exception as e:
            context = {
                'info': '删除失败'
            }

            return render(request, 'myadmin/user/info.html', context)


class EditVariety(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            shop_name = Shop.objects.get(id=product.shop_id).name
            category_name = Category.objects.get(id=product.category_id).name
            product.shop_name = shop_name
            product.category_name = category_name
            context = {
                'product': product,
            }

            return render(request, 'myadmin/food/editvariety.html', context)
        except Exception as e:
            context = {
                'info': '编辑失败',
            }
            print(e)
            return render(request, 'myadmin/user/info.html', context)

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        price = request.POST.get('price')
        variety_name = request.POST.get('variety_name')
        product_status = request.POST.get('status')

        if not all([product_status, price, variety_name]):
            context = {
                'info': '编辑失败',
            }
            return render(request, 'myadmin/user/info.html', context)

        product.price = price
        product.status = product_status
        product.name = variety_name
        product.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        product.save()

        context = {
            'info': '编辑成功',
        }
        return render(request, 'myadmin/user/info.html', context)

