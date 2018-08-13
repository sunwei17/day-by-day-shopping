#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from models import UserInfo
from django.core.urlresolvers import reverse
import hashlib
from df_user import user_decorator
from df_goods.models import GoodsInfo
#
def order(request):
    return render(request,'user_center_order.html')
def logout(request):
    request.session.flush()
    return redirect('/goods/index')
@user_decorator.login
def site(request):
    uid = request.session['user_id']
    user=UserInfo.objects.get(id=uid)
    if request.method=='POST':
        post= request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context={'user':user,'page_name':1,}
    return render(request,'user_center_site.html',context)
@user_decorator.login
def uinfo(request):
    uid=request.session['user_id']
    User=UserInfo.objects.filter(id=uid)
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_list = []
    if goods_ids!='':
        goods_ids1=goods_ids.split(',')

        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context={'uemail':User[0].uemail,
             'goods_list':goods_list

             }
    return  render(request,'user_center_info.html',context)
def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname,'upwd':''}
    return render(request,'login.html',context)
def login_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)#前段选中为1，这里默认为0
    users=UserInfo.objects.filter(uname=uname)#get不存在异常报错
    if len(users)==1:
        s1=hashlib.md5()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','index')
            red=HttpResponseRedirect(url)
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=100)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context={'title':'登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'login.html',context)
    else:
        context={'title':'登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'login.html',context)
def register_exist(request):
    uname=request.GET['uname']
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})
    #return HttpResponse('wu')
@user_decorator.login
def index(request):
    context={'guest_cart':0,'page_name':1}
    return render(request,'index.html',context)
def logincheck(request):
    upwd=request.POST['pwd']
    uname=request.POST['username']
    request.session['uname'] = uname
    request.session['upwd'] = upwd
    s = hashlib.md5()
    s.update(upwd)

    list=UserInfo.objects.filter(upwd=s.hexdigest(),uname=uname)
    if list.__len__()>0:
        return redirect(reverse('register:index'))
    return  redirect(reverse('register:login'))
def login2(request):
    uname=''
    upwd=''
    if request.COOKIES.has_key('uname'):
        context={'uname':request.session['uname'],'upwd':request.session['upwd']}

        return render(request,'login.html',context)
    else :
        return render(request, 'login.html')

def register(request):
    return render(request,'register.html')
def saveregister(request):
    try :
        uname= request.POST['user_name']
        upwd=request.POST['pwd']
        s = hashlib.md5()
        s.update(upwd)

        request.session['uname']=uname
        request.session['upwd']=upwd
        uemail=request.POST['email']
        user=UserInfo()
        user2=user.create(uname.encode("utf-8"),s.hexdigest(),uemail)
        user2.save()
        return redirect(reverse('register:login'))
    except:
        return  HttpResponse(u'失败!'+uname)
