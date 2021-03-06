from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Q
from myadmin.models import User
import hashlib, random, datetime


class VIPadmin(View):
    '''会员管理类'''
    def get(self, request, page=1):
        ulist = User.objects.all().order_by('id')
        mywhere = []

        content = request.GET.get('table_search', None)
        if content:
            ulist = User.objects.filter(Q(username__contains=content) | Q(nickname__contains=content)).order_by('id')
            mywhere.append('table_search=' + content)  # 封装搜索条件 防止在分页之后点击下一页 搜索条件失效

        paginator = Paginator(ulist, 5)
        page = int(page)
        maxindex = paginator.num_pages  # 获取最大列表数

        if page > maxindex:
            page = maxindex
        if page < 1:
            page = 1

        pagecontext = paginator.page(page)  # 当前页数据
        prange = paginator.page_range  # 获取分页页码列表

        context = {
            'ulist': pagecontext,
            'all_page': prange,
            'page': page,
            'maxpage': maxindex,
            'mywhere': mywhere,
        }

        return render(request, 'myadmin/user/member.html', context)


class AddVIP(View):
    def get(self, request):
        return render(request, 'myadmin/user/add.html')

    def post(self, request):
        try:
            user = request.POST.get('user')
            username = request.POST.get('username')
            n = random.randint(100000, 999999)
            pwd = request.POST.get('pwd') + str(n)

            # 进行密码加密
            md5 = hashlib.md5()
            md5.update(pwd.encode('UTF-8'))

            addUer = User()
            addUer.username = user
            addUer.nickname = username
            addUer.password_hash = md5.hexdigest()
            addUer.password_salt = n
            addUer.status = 1
            addUer.create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addUer.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            addUer.save()
            context = {'info': '保存成功'}
        except Exception as e:
            context = {'info': '保存失败'}

        return render(request, 'myadmin/user/info.html', context)


class DelVIP(View):
    '''
    删除员工
    '''
    def get(self, request, userid):
        try:
            # page = request.GET.get('page')
            delid = User.objects.get(id=userid)
            delid.delete()
            context = {'info': '删除成功'}
        except Exception as e:
            context = {'info': '删除失败'}

        return render(request, 'myadmin/user/info.html', context)
        # return redirect(reverse('myadmin:VIP', kwargs={'page': page}))  # 删除成功之后还留在原来的页码面、


class EditVIP(View):
    def get(self, request, userid):
        try:
            uid = User.objects.get(id=userid)
            context = {'uid': uid}
            return render(request, 'myadmin/user/edit.html', context)
        except Exception as e:
            context = {'info': '修改信息错误'}
            print(e)
            return render(request, 'myadmin/user/info.html', context)

    def post(self, request, userid):
        username = request.POST.get('user')
        nickname = request.POST.get('username')
        status = request.POST.get('status')

        try:
            uVIP = User.objects.get(id=userid)
            uVIP.username = username
            uVIP.nickname = nickname
            uVIP.status = status
            uVIP.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            uVIP.save()

            context = {'info': '修改成功'}
        except Exception as e:
            context = {'info': '修改失败'}

        return render(request, 'myadmin/user/info.html', context)



