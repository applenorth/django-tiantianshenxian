#-*- coding:utf-8 -*-
"""
@Time:2020/9/3010:47
@Auth:DaiXvWen
@File:urls.py
"""
#从Store中导入所有视图
from .views import *
from django.urls import path,include

#ViewSet类提供的路由器
from rest_framework.routers import DefaultRouter
from Store.serializer import *
router=DefaultRouter()
#收集注册路由，注册路由器
router.register("morelist",MoreListView,basename="")
router.register("select_all_list",SelectAllListView,basename="")
# #ViewSet类的路由
# more_list = MoreListView.as_view(
#     {'get': 'list'}
# )

urlpatterns = [
    path('index/', index),                                      #后台管理：首页
    path('add_goods/', add_goods),                              #后台管理：添加商品
    path('orders/', orders),                                    #后台管理：订单确认
    path('count_goods/', count_goods),                          #后台管理：商品统计界面
    path('count_orders/', count_orders),                        #后台管理：订单统计界面
    path('store/', store),                                      #后台管理：店铺管理
    path('login/', login),                                      #后台管理：登录界面
    path('register/', register),                                #后台管理：注册界面
    path('logout/', logout),                                    #后台管理：登出路由
    path('userinfo/', userinfo),                                #后台管理：店铺用户信息
    path('userinfoview/', UserinfoView.as_view()),              #后台管理：个人信息api接口
    path('goodsview/', GoodsView.as_view()),                    #后台管理：商品信息接口

    # path('add_goods/', add_goods),

    # path("morelist/",MoreListView.as_view())  #ApiView类路由
    path("api/", include(router.urls)),
    # path("morelist/", more_list),

    path("captcha/", captcha),                                   #后台管理：验证码路由
    path("paginationview/", PaginationView.as_view()),           #分页的goods_list路由

]