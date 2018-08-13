from django.conf.urls import include, url
from df_goods import views
from views import MySearchView
urlpatterns = [

    url(r'^index$',views.index,name='index'),
    url(r'^detail(\d+)$',views.detail,name='detail'),
    url(r'^list(\d+)_(\d+)_(\d+)$',views.list,name='list'),
    url(r'^search/', MySearchView()),

]