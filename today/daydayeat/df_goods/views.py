#coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator
from models import *
from df_cart.models import CartInfo
from df_user import user_decorator
# Create your views here.
def detail(request,id):
    goods=GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={'guest_cart':1,
             'g':goods,
             'news':news,
             'id':id,
             }
    response= render(request,'detail.html',context)
    goods_ids=request.COOKIES.get('goods_ids','')#存5个历史记录
    goods_id=id
    if goods_ids != '':
        goods_ids1=goods_ids.split(',')
        if goods_ids1.count(goods_id)>=1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)
        if len(goods_ids1)>=6:
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)
    else:
        goods_ids=goods_id
    response.set_cookie('goods_ids',goods_ids)
    return response
def list(request,tid,pindex,sortby):
    type1=TypeInfo.objects.get(id=tid)
    if sortby=='1' :
        goodss=GoodsInfo.objects.filter(gtype_id=tid).order_by('id')
    if sortby=='2':
        goodss = GoodsInfo.objects.filter(gtype_id=tid).order_by('gprice')
    else:
        goodss = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gclick')
    news=type1.goodsinfo_set.order_by('-id')[0:2]
    paginator=Paginator(goodss,2)
    page=paginator.page(int(pindex))
    context={
        'guest_cart':1,
        'page_name':1,
        'sort':sortby,
        'tid':tid,
        'goodss':goodss,
        'type1':type1,
        'page':page,
        'paginator':paginator,
        'news':news,
             }

    return render(request,'list.html',context)
def index(request):
    typelist=TypeInfo.objects.all()
    list=[]
    list2=[]
    for goods in typelist:
        g=goods.goodsinfo_set.order_by('-id')
        if len(g)>0:
            if len(g)>4:
                lenn=4
            else :
                lenn=len(g)
            gg=goods.goodsinfo_set.order_by('-gclick')
            if len(gg)>4:
                len2=4
            else :
                len2=len(gg)
            list.append(g[0:lenn])
            list2.append(gg[0:len2])
    #type0=typelist[0].goodsinfo_set.order_by('-id')[0:4]
    #type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    #tlist=['新鲜水果','海鲜','蔬菜']
    context={
        'title':'首页',
        'guest_cart':1,
        'page_name':1,
        'list':list,
        'list2':list2,
        #'tlist':tlist,
    }
    return render(request,'index.html',context)
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id'])
    else:
        return 0
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context=super(MySearchView,self).extra_context()
        context['title']='搜索'
        context['guest_cart']=1
        context['cart_count']=cart_count(self.request)
        return context