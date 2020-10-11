from django.db import models

# Create your models here.

GENDER_LIST=(
    (0,'女'),
    (1,'男')
)


class QUser(models.Model):
    """用户模型"""
    username = models.CharField(max_length=32, verbose_name="账号", unique=True)
    password = models.CharField(max_length=32, verbose_name="密码")
    nickname = models.CharField(max_length=32, verbose_name="昵称", null=True, blank=True)
    gender = models.IntegerField(verbose_name="性别", default=1,choices=GENDER_LIST)
    phone = models.CharField(max_length=32, verbose_name="电话", null=True, blank=True)
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True)
    picture = models.ImageField(upload_to="quser_images", verbose_name="后台用户头像", default="1.jpg")
    address = models.TextField(verbose_name="地址", default="")
    usertype = models.IntegerField(verbose_name="用户类型", default=0)  # 0代表买家， 1代表卖家

    class Meta:
        db_table = "quser"


class Store(models.Model):
    """商铺模型"""
    s_name = models.CharField(max_length=32, verbose_name="商铺名")

    s_logo = models.ImageField(upload_to="store_images", verbose_name="用户店铺图片", default="1.jpg")

    s_address = models.TextField(verbose_name="商铺地址")
    s_description = models.TextField(verbose_name="商铺描述")
    s_user = models.OneToOneField(to=QUser, on_delete=models.CASCADE)

    s_changed_datetime=models.DateTimeField(verbose_name="店铺名修改时间",auto_now=False)

    class Meta:
        db_table = "store"


class GoodsType(models.Model):
    """商品类型"""
    t_name = models.CharField(max_length=32, verbose_name="类型名")
    t_description = models.TextField(verbose_name="类型描述")
    t_img = models.CharField(max_length=64, verbose_name="类型图片")

    class Meta:
        db_table = "goodstype"

class Goods(models.Model):
    """商品"""
    g_name = models.CharField(max_length=32, verbose_name="商品名")
    g_number = models.IntegerField(verbose_name="商品编号")
    g_price = models.FloatField(verbose_name="单价")

    g_safe_date = models.IntegerField(verbose_name="保质期")
    g_public_date=models.DateField(verbose_name="生产日期",auto_now=True)

    g_description = models.TextField(verbose_name="描述")
    g_picture = models.ImageField(upload_to="goods_images", verbose_name='商品图片')
    g_num = models.IntegerField(verbose_name="商品库存")
    g_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE)
    # 店铺关系
    g_store = models.ForeignKey(to=Store, on_delete=models.CASCADE)

    class Meta:
        db_table = "goods"


class GoodsImg(models.Model):
    """商品图片"""
    img_path = models.CharField(max_length=32, verbose_name="图片路径")
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)

    class Meta:
        db_table = "goodsimg"



