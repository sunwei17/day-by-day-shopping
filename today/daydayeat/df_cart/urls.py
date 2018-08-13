from django.conf.urls import include, url
from df_cart import views
urlpatterns = [

    url(r'^cart$',views.cart,name='cart'),
    url(r'^add(\d+)_(\d+)$',views.add,name='add'),
    url(r'^edit(\d+)_(\d+)$',views.edit),
    url(r'^delete(\d+)/$',views.delete),


]