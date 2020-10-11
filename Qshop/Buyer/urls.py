#-*- coding:utf-8 -*-
"""
@Time:2020/9/3010:48
@Auth:DaiXvWen
@File:urls.py
"""

# 从Store中导入所有视图
from django.urls import path,include,re_path
from Buyer.views import *

# from rest_framework.routers import DefaultRouter
# from Buyer.serializer import *
# router=DefaultRouter()
# #收集注册路由，注册路由器
# router.register("morelist",MoreListView,basename="")

urlpatterns = [
    path('index/', index),                          #前台页面：首页
    path('login/', login),                          #前台页面：登录界面
    path('register/', register),                    #前台页面：注册界面
    path('cart/', cart),                            #前台页面：购物车
    path('edit_address/', edit_address),            #前台页面：修改地址
    path('edit_user/', edit_user),                  #前台页面：修改用户信息
    path('myorders/', myorders),                    #前台页面：我的订单
    path('usercenterinfo/', usercenterinfo),        #前台页面：个人用户中心页面
    path('list/', list),                            #前台页面：列表页面展示
    re_path('detail/(\w*)/', detail),               #前台页面：商品详情页面
    path('logout/', logout),                        #前台页面：登出路由
    path('place_order/', place_order),              #前台页面：订单结算页面
]