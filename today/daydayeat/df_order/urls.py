from django.conf.urls import include, url
from df_order import views
urlpatterns = [

    url(r'^order$',views.order,name='order'),
    url(r'^test$', views.test, name='test'),
    url(r'^order_handle$',views.order_handle,name='order_handle'),



]