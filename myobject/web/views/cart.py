from django.shortcuts import render, redirect, reverse, HttpResponse


# todo:添加商品
def addcart(request, pid):
    product = request.session['productlist'][pid]
    product['num'] = 1

    cartlist = request.session.get('cartlist', {})

    if pid in cartlist:
        cartlist[pid]['num'] += product['num']
    else:
        # 如果pid不再购物车里 就需要将商品整体 动态添加到购物车里
        cartlist[pid] = product

    request.session['cartlist'] = cartlist
    return redirect(reverse('web:web_index'))


# todo:删除购物车商品
def delcart(request, pid):
    product = request.session['productlist'][pid]
    cartlist = request.session.get('cartlist', {})

    if pid in cartlist:
        del cartlist[pid]

    request.session['cartlist'] = cartlist
    return redirect(reverse('web:web_index'))


# todo:清空购物车
def clearcart(request):

    del request.session['cartlist']

    return redirect(reverse('web:web_index'))


# todo:增加减少商品
def changecart(request, pid):
    # 获取增加减少操作
    num = request.GET.get('num')
    cartlist = request.session.get('cartlist', {})

    if pid in cartlist:
        cartlist[pid]['num'] += int(num)

    # 防止商品数量少于0
    if cartlist[pid]['num'] < 0:
        cartlist[pid]['num'] = 0

    request.session['cartlist'] = cartlist

    return redirect(reverse('web:web_index'))
