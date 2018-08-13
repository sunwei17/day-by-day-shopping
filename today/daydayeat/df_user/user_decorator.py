#coding=utf-8
from django.shortcuts import HttpResponseRedirect
#判断登录，装饰类
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            red=HttpResponseRedirect('login')
            red.set_cookie('url',request.get_full_path())#提取url到cookie
            return red
    return login_fun
'''
request.path:表示当前路径，无参数返回
request.get_full_path:表示完整路径，包括额外参数
'''