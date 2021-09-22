from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from myadmin.models import Member
import datetime
import time


class MemberView(View):
    def get(self, request, page):
        members = Member.objects.all().order_by('id')
        mywhere = []

        table_search = request.GET.get('table_search')

        if table_search:
            members = Member.objects.filter(nickname__contains=table_search)
            mywhere.append('table_search=' + table_search)

        paginator = Paginator(members, 10)
        page = int(page)
        maxindex = paginator.num_pages

        if page > maxindex:
            page = maxindex
        if page < 1:
            page = 1

        pagecontext = paginator.page(page)  # 指定分页信息
        pagerange = paginator.page_range  # 分页列表

        context = {
            'members': pagecontext,
            'pagerange': pagerange,
            'maxindex': maxindex,
            'page': page,
            'mywhere': mywhere,
        }

        return render(request, 'myadmin/member/member.html', context)


class DelMember(View):
    def get(self, request, member_id):
        try:
            del_member = Member.objects.get(id=member_id)
            del_member.delete()

            context = {
                'info': '删除成功'
            }

            return render(request, 'myadmin/user/info.html', context)
        except Exception as e:
            context = {
                'info': '删除失败'
            }

            return render(request, 'myadmin/user/info.html', context)


class EditMember(View):
    def get(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)

            context = {
                'member': member,
            }

            return render(request, 'myadmin/member/editmember.html', context)
        except Exception as e:
            context = {
                'info': '编辑失败',
            }
            print(e)
            return render(request, 'myadmin/user/info.html', context)

    def post(self, request, member_id):
        member = Member.objects.get(id=member_id)
        base_img = member.avatar
        mobile = request.POST.get('phone')
        status = request.POST.get('status')
        avatar = request.FILES.get('avatar', base_img)

        if not all([mobile, status]):
            context = {
                'info': '编辑失败',
            }
            return render(request, 'myadmin/user/info.html', context)

        # 未选择头像就使用原有的头像
        if type(avatar) != str:
            avatar = str(time.time()) + '.' + avatar.name.split('.').pop()
            with open(f'static/uploads/member/{avatar}', 'wb+') as f:
                for chunk in avatar.chunks():
                    f.write(chunk)

        member.mobile = mobile
        member.status = status
        member.avatar = avatar
        member.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        member.save()

        context = {
            'info': '编辑成功',
        }
        return render(request, 'myadmin/user/info.html', context)

