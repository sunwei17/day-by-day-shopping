from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from models import *
from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from df_user import user_decorator
# Create your views here.
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count}
    return JsonResponse(data)

def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)

def cart(request):
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)
    count=carts.count()
    context={
        'page_name':1,
        'cart':carts,
        'count1':count
    }
    return  render(request,'cart.html',context)
@user_decorator.login
def add(request,g_id,g_count):
    uid=request.session['user_id']
    cart1=CartInfo()
    shangpin=CartInfo.objects.filter(id=g_id)
    if len(shangpin)>=1:
        cart1=shangpin[0]
        cart1.count=cart1.count+int(g_count)
    else:
        cart1.goods=GoodsInfo.objects.filter(id=g_id)[0]
        cart1.user=UserInfo.objects.filter(id=uid)[0]
        cart1.count=g_count
    cart1.save()
    if request.is_ajax():
        count=CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count':count})
    else:
        return redirect(reverse('cart:cart'))#redirect('/cart/')
