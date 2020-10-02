#-*- coding:utf-8 -*-
"""
@Time:2020/9/3010:48
@Auth:DaiXvWen
@File:urls.py
"""

# 从Store中导入所有视图
from django.urls import path,include
from Buyer.views import *

# from rest_framework.routers import DefaultRouter
# from Buyer.serializer import *
# router=DefaultRouter()
# #收集注册路由，注册路由器
# router.register("morelist",MoreListView,basename="")

urlpatterns = [
    path('index/', index),
    path('login/', login),
    path('register/', register),
    path('cart/', cart),
    path('edit_address/', edit_address),
    path('edit_user/', edit_user),
    path('myorders/', myorders),
    path('place_order/', place_order),
    path('usercenterinfo/', usercenterinfo),
    path('list/', list),

]