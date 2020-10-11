#-*- coding:utf-8 -*-
"""
@Time:2020/9/2914:50
@Auth:DaiXvWen
@File:serializer.py
"""
from rest_framework import serializers
from Store.models import *
#序列化器
#搭建一个关于goods的api接口
class MoreListSeriaLizer(serializers.ModelSerializer):  #继承serializers.ModelSerializer父类
    class Meta:
        model=Goods    #要序列化的模型
        #要序列化的字段
        fields="__all__"    #所有，序列化模型中的所有字段
        # fields=["g_name","g_price"]   #序列化需要的字段



#api视图类
#ApiView
from rest_framework.views import APIView,Response
class MoreListView1(APIView):
    #处理get请求
    def get(self,request):
        #返回10条数据
        #编写查询语句，拿到数据
        goods_list=Goods.objects.all()[:10]
        #将结构使用MoreListSeriaLizer序列化
        serialize=MoreListSeriaLizer(goods_list,many=True)   #many=True 结果中使用列表的形式，多个
        result=serialize.data  #要返回的数据
        return Response(result)

##minxins类
from rest_framework import mixins,generics
class MoreListView2(mixins.ListModelMixin,generics.GenericAPIView):
    def get_queryset(self):
        #获取到一个queryset结果
        #拿到type_id
        type_id=self.request.GET.get("type_id")
        goods_list=GoodsType.objects.filter(id=type_id).first().goods_set.all()

        #抛出goods_list
        return goods_list

    #序列化器
    serializer_class=MoreListSeriaLizer
    def get(self,request,*args,**kwargs):
        #处理get请求
        return self.list(request,*args,**kwargs)
    #返回数据，让结果保持原有的样子
    def get_serializer_context(self):
        return{
            "view":self
        }

#通用视图类
#视图
from rest_framework import generics
class MoreListView3(generics.ListAPIView):
    #创建获取queryset类
    def get_queryset(self):
        type_id = self.request.GET.get("type_id")
        goods_list = GoodsType.objects.filter(id=type_id).first().goods_set.all()

        # 抛出goods_list
        return goods_list

    # 序列化器
    serializer_class = MoreListSeriaLizer

    # 返回数据，让结果保持原有的样子
    def get_serializer_context(self):
        return {
            "view": self
        }

##ViewSet类和路由器
#视图，获取登录用户的所有商品信息
from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination

class MoreListView(viewsets.ReadOnlyModelViewSet):  #viewsets.ReadOnlyModelViewSet
    def get_queryset(self):
        #拿到登录用户的所有商品信息
        quser_id = self.request.GET.get("quser_id")

        quser_store = QUser.objects.filter(id=quser_id).first().store
        store_id = quser_store.id
        #通过店铺查询店铺中所有的商品
        goods_list=Goods.objects.filter(g_store_id=store_id).all()

        # goods_list = GoodsType.objects.filter(id=quser_id).first().goods_set.all()

        # 抛出goods_list
        return goods_list

        # 序列化器

    serializer_class = MoreListSeriaLizer

    # 返回数据，让结果保持原有的样子
    def get_serializer_context(self):
        return {
            "view": self
        }


#为前台购物界面显示所有数据提供接口
#返回所有商品
class SelectAllListView(viewsets.ReadOnlyModelViewSet):  #viewsets.ReadOnlyModelViewSet
    def get_queryset(self):
        #拿到登录用户的所有商品信息

        goods_list=Goods.objects.all()

        # goods_list = GoodsType.objects.filter(id=quser_id).first().goods_set.all()
        # 抛出goods_list
        return goods_list

        # 序列化器

    serializer_class = MoreListSeriaLizer

    # 返回数据，让结果保持原有的样子
    def get_serializer_context(self):
        return {
            "view": self
        }

#自定义分页器：PageNumberPagination  看第n页，每页显示n条数据
#拿到指定用户的商品，并12条数据一页进行分页
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination,CursorPagination
class MyPageNumber(PageNumberPagination):
    page_size = 12  # 每页显示多少条
    page_size_query_param = 'size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = None  # 最大页码数限制

#返回带页码连接的响应
class PaginationView(APIView):
    def get(self, request):

        # 拿到登录用户的所有商品信息
        quser_id = self.request.GET.get("quser_id")

        quser_store = QUser.objects.filter(id=quser_id).first().store
        store_id = quser_store.id
        # 通过店铺查询店铺中所有的商品
        goods_list = Goods.objects.filter(g_store_id=store_id).all()


        # 分页
        page_obj = MyPageNumber()
        page_article = page_obj.paginate_queryset(queryset=goods_list, request=request, view=self)

        ret = MoreListSeriaLizer(page_article, many=True)
        # return Response(ret.data)
        # 返回带超链接 需返回的时候用内置的响应方法
        return page_obj.get_paginated_response(ret.data)
