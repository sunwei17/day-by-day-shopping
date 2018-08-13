#coding=utf-8
from django.shortcuts import render,redirect
from df_cart.models import *
from df_user.models import *
from df_order.models import *
from django.db import transaction
from django.http import HttpResponse,JsonResponse
import datetime
from decimal import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def test(request):
    cids = request.POST.get('str1','')
    return redirect(cids+'.html')#HttpResponse('nihao')
def order(request):
    list=request.GET.getlist('cart_id')
    glist=[]
    for item in list:
        glist.append(CartInfo.objects.filter(id=int(item))[0])
    uid=request.session['user_id']
    user1=UserInfo.objects.get(pk=int(uid))
    address=user1.uaddress+' '+user1.ushou+' '+user1.uphone
    context={'glist':glist,'list':list,'address':address,}
    return  render(request,'place_order.html',context)

@transaction.atomic()
def order_handle(request):
    tran_id=transaction.savepoint()
    cids = str(request.POST.get('str1',''))#默认空
    cidlist = cids.split('a')
    ccc=cidlist[0:(len(cidlist)-1)]

    try:
        uid = request.session['user_id']
        od=OrderInfo()
        now=datetime.datetime.now()
        od.odate=now
        od.oaddress=request.POST.get('ad','')
        od.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        od.user_id=uid
        od.ototal=Decimal(request.POST.get('ot',''))
        od.save()

        for c in ccc :
            ox = OrderDetailInfo()
            ox.order=od
            cart=CartInfo.objects.get(id=c)
            goods=cart.goods
            if goods.gkucun>=cart.count:
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()
                ox.goods_id=goods.id
                ox.price=goods.gprice
                ox.count=cart.count
                ox.save()

                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                data = {'ok': 1}#错
                return JsonResponse(data)#redirect('/cart/cart')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print "+++++++++%s"%e
        transaction.savepoint_rollback(tran_id)
        data = {'ok': 1}#错
        return JsonResponse(data)
    data = {'ok': 2}#成功
    return JsonResponse(data)#redirect('/register/order')
