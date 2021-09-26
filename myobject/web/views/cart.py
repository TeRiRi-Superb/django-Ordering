from django.shortcuts import render, redirect, reverse, HttpResponse


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


def delcart(request, pid):
    pass


def clearcart(request):
    pass


def changecart(request):
    pass