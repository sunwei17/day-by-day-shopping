#coding=utf-8
from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('df_user.UserInfo')#关联其他模型类
    goods=models.ForeignKey('df_goods.GoodsInfo')
    count=models.IntegerField()