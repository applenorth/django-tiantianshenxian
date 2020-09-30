from django.db import models

# Create your models here.
GENDER_STATUS={
    (0,'女'),
    (1,'男')
}


class StoreUser(models.Model):
    #不需要定义id字段，会自动生成
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=32,verbose_name="密码")
    nick_name=models.CharField(max_length=32,verbose_name="昵称")
    age=models.IntegerField(verbose_name="年龄",default=0)
    gender=models.IntegerField(verbose_name="性别(0-女，1-男)",choices=GENDER_STATUS,default=1)
    email=models.EmailField(verbose_name="邮箱",null=True)
    address=models.TextField(verbose_name="地址",null=True)
    create_time=models.DateTimeField(verbose_name="创建时间",auto_now=True)
    class Meta:
        db_table="storeuser"

#创建店铺表，与StoreUser表为一对一关系
class Store(models.Model):
    store_name=models.CharField(max_length=32,verbose_name="店铺名")
    store_desc=models.TextField(verbose_name="店铺描述")
    store_address=models.TextField(verbose_name="店铺地址")

    store_user=models.OneToOneField(to=StoreUser,on_delete=models.CASCADE)

    ##on_delete=代表关联表的数据被删除后，另一张表的对应数据，该如何处理
    # models.CASCADE 如果删除关联表的数据，对应表的数据也会被删除
    # models.PROTECT 如果有外键不允许删除
    #to= 代表和哪种模型有关系

    class Meta:
        db_table="store"

#创建商品类型表
class GoodsType(models.Model):

    t_name = models.CharField(max_length=32,verbose_name="类型名字")
    t_desc = models.TextField(verbose_name="类型描述")
    class Meta:
        db_table = "goods_type"

#创建商品表
class Goods(models.Model):

    goods_name = models.CharField(max_length=32,verbose_name="商品名字")
    goods_num = models.IntegerField(verbose_name="商品数量")
    goods_price = models.FloatField(verbose_name="商品单价")
    goods_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE)
    class Meta:
        db_table = "goods"


