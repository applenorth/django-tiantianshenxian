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

# #ViewSet类的路由
# more_list = MoreListView.as_view(
#     {'get': 'list'}
# )

urlpatterns = [
    path('index/', index),
    path('add_goods/', add_goods),
    path('orders/', orders),
    path('count_goods/', count_goods),
    path('count_orders/', count_orders),
    path('store/', store),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('userinfo/', userinfo),
    path('userinfoview/', UserinfoView.as_view()),

    # path('add_goods/', add_goods),

    # path("morelist/",MoreListView.as_view())  #ApiView类路由
    path("api/", include(router.urls)),
    # path("morelist/", more_list),

]