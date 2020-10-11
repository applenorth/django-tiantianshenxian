from Store.models import *
from django.db import models

# Create your models here.

##创建订单表与订单详情表
class PlaceOrder(models.Model):
    """
    订单表，一表
    """
    order_num = models.CharField(max_length=32,verbose_name="订单编号")
    order_status = models.IntegerField(default=0,verbose_name="订单状态")  # 0 代表未支付  1 代表已支付   2 发货中
    type_number = models.IntegerField(default=0,verbose_name="商品数量")
    total_price = models.FloatField(verbose_name="订单总金额")
    # order_address = models.ForeignKey(to=RecvAddress,on_delete=models.CASCADE,verbose_name="收货地址")
    user_id = models.ForeignKey(to=QUser,on_delete=models.CASCADE,verbose_name="买家")
    class Meta:
        db_table="placeorder"


class OrderInfo(models.Model):
    """
    订单详情表，多表
    """
    goods_name = models.CharField(verbose_name="商品名字",max_length=32)
    goods_price = models.FloatField(verbose_name="商品单价")
    goods_num = models.IntegerField(verbose_name="商品数量")
    goods_picture = models.CharField(max_length=64,verbose_name="商品图片")
    goods_total = models.FloatField(verbose_name="商品小计")
    goods_status =models.IntegerField(verbose_name="商品状态")
    store = models.ForeignKey(to=Store,on_delete=models.CASCADE)
    order = models.ForeignKey(to=PlaceOrder,on_delete=models.CASCADE)
    class Meta:
        db_table = "orderinfo"

