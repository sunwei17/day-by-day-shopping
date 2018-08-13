from django.conf.urls import include, url
import  views
urlpatterns = [
    url(r'^login$',views.login,name='login'),
    url(r'^order$',views.order,name='order'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^findex$',views.index,name='index'),
    url(r'^userinfo$',views.uinfo,name='uinfo'),
    url(r'^site$',views.site,name='site'),
    url(r'^logincheck$',views.logincheck,name='logincheck'),
    url(r'^register$',views.register,name='register'),
    url(r'^register_exist/$',views.register_exist,name='register_exist'),
    url(r'^saveregister$',views.saveregister,name='saveregister'),
    url(r'^login_handle$',views.login_handle,name='login_handle'),

]
