# 菜品信息
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from myadmin.models import Shop, Category
import datetime


class CateGoryView(View):
    def get(self, request, page):
        cates = Category.objects.all()

        search = request.GET.get('table_search')
        mywhere = []

        if search:
            cates = Category.objects.filter(name__contains=search)
            mywhere.append('table_search=' + search)

        try:
            for cate in cates:
                shop_id = cate.shop_id
                shop_name = Shop.objects.get(id=shop_id).name

                cate.shop_name = shop_name
        except Exception as e:
            print('数据错误')

        paginator = Paginator(cates, 10)
        page = int(page)
        maxindex = paginator.num_pages

        if page > maxindex:
            page = maxindex
        if page < 1:
            page = 1

        pagecontext = paginator.page(page)
        pagerange = paginator.page_range

        context = {
            'cates': pagecontext,
            'pagerange': pagerange,
            'maxindex': maxindex,
            'page': page,
            'mywhere': mywhere,
        }

        return render(request, 'myadmin/food/category.html', context)


class DelCategory(View):
    def get(self, request, cate_id):
        try:
            del_cate = Category.objects.get(id=cate_id)
            del_cate.delete()

            context = {
                'info': '删除成功'
            }

            return render(request, 'myadmin/user/info.html', context)
        except Exception as e:
            context = {
                'info': '删除失败'
            }

            return render(request, 'myadmin/user/info.html', context)


class EditCategory(View):
    def get(self, request, cate_id):
        try:
            cate = Category.objects.get(id=cate_id)
            shop_name = Shop.objects.get(id=cate.shop_id).name
            cate.shop_name = shop_name
            context = {
                'cate': cate,
            }

            return render(request, 'myadmin/food/updatecate.html', context)
        except Exception as e:
            context = {
                'info': '编辑失败',
            }
            print(e)
            return render(request, 'myadmin/user/info.html', context)

    def post(self, request, cate_id):
        cate = Category.objects.get(id=cate_id)
        cate_name = request.POST.get('name')
        cate_status = request.POST.get('status')

        if not all([cate_name, cate_status]):
            context = {
                'info': '编辑失败',
            }
            return render(request, 'myadmin/user/info.html', context)

        cate.name = cate_name
        cate.status = cate_status
        cate.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cate.save()

        context = {
            'info': '编辑成功',
        }
        return render(request, 'myadmin/user/info.html', context)


class AddCategory(View):
    def get(self, request):
        shops = Shop.objects.all()
        context = {
            'shops': shops
        }
        return render(request, 'myadmin/food/addcategory.html', context)

    def post(self, request):
        shop_id = request.POST.get('shop')
        name = request.POST.get('name')

        context = {
            'info': '添加成功'
        }

        return render(request, 'myadmin/user/info.html', context)