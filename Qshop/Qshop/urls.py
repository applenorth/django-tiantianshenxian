"""Qshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Store.views import *
from Store.serializer import *
#ViewSet类提供的路由器
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
#收集注册路由，注册路由器
router.register("morelist",MoreListView,basename="")


# #ViewSet类的路由
# more_list = MoreListView.as_view(
#     {'get': 'list'}
# )
urlpatterns = [
    path('admin/', admin.site.urls),

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
    path('jsontest/', jsontest),
    path('vuedemo/', vuedemo),
    path('ajaxdemo/', ajaxdemo),
    path('list/', list),
    # path('add_goods/', add_goods),

    # path("morelist/",MoreListView.as_view())  #ApiView类路由
    path("api/", include(router.urls)),
    # path("morelist/", more_list),

]
