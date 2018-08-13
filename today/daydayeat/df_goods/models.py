#coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class TypeInfo(models.Model):
    title=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return self.title.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='df_goods')
    gprice=models.DecimalField(max_digits=5,decimal_places=2)
    isDelete=models.BooleanField(default=False)
    gunit=models.CharField(max_length=20,default='500g')
    gclick=models.IntegerField()#点击量销量，减轻数据库压力否则就得用聚合函数压力大
    gjianjie=models.CharField(max_length=255)
    gkucun=models.IntegerField()#维护库存
    gcontent=HTMLField()
    gtype=models.ForeignKey(TypeInfo)
    #gadv=models.BooleanField(default=False)#推荐商品指数