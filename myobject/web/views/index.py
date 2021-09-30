from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from myadmin.models import User, Shop, Category, Product
import hashlib


class IndexView(View):
    def get(self, request):
        cartlist = request.session.get('cartlist', {})
        total_mo = 0

        for cart in cartlist.values():
            print(cart)
            total_mo += cart['num'] * cart['price']

        request.session['total_mo'] = total_mo

        context = {'categorylist': request.session.get("categorylist", {}).items()}
        return render(request, 'web/index.html', context)


class LoginView(View):
    def get(self, request):
        shops = Shop.objects.filter(status=1).order_by('id')
        context = {
            'shops': shops
        }
        return render(request, 'web/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        pwd = request.POST.get('pass')
        code = request.POST.get('code')
        verifycode = request.session['verifycode']
        shop_id = request.POST.get('shop_id')

        if not all([username, pwd, code, shop_id]):
            context = {
                'info': '账号或密码错误'
            }

            return render(request, 'web/login.html', context)

        try:
            shops = Shop.objects.filter(status=1).order_by('id')
            user = User.objects.get(username=username)
            # 记录店铺信息
            shop = Shop.objects.get(id=shop_id)
            request.session['shop_name'] = shop.toDict()

            if verifycode == code:
                # 解码密码
                md5 = hashlib.md5()
                password = pwd + user.password_salt
                md5.update(password.encode('UTF-8'))

                categorys = Category.objects.filter(shop_id=shop_id, status=1)
                categorylist = dict()  # 菜品类别（内含有菜品信息）
                productlist = dict()  # 菜品信息

                if user.password_hash == md5.hexdigest():
                    # 将user的信息转换成字典存入session
                    request.session['web_user'] = user.toDict()
                    for category in categorys:
                        c = {'c_id': category.id, 'name': category.name, 'pid': []}
                        plist = Product.objects.filter(category_id=category.id, status=1)
                        for p in plist:
                            c['pid'].append(p.toDict())
                            productlist[p.id] = p.toDict()
                        categorylist[category.id] = c

                    request.session['categorylist'] = categorylist
                    request.session['productlist'] = productlist
                    return redirect(reverse('web:web_index'))
                else:
                    context = {'info': '账号或密码错误',
                               'shops': shops
                               }
            else:
                context = {'info': '验证码错误',
                           'shops': shops
                           }

        except Exception as e:
            context = {
                'info': '账号或密码错误',
                'shops': shops,
            }

        return render(request, 'web/login.html', context)


def logout(request):
    del request.session['web_user']
    del request.session['shop_name']
    del request.session['cartlist']
    return redirect(reverse('web:web_login'))


def verify(request):
    '''生成验证码 '''
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')