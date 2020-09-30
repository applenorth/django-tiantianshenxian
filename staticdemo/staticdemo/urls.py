"""staticdemo URL Configuration

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
from django.urls import path,re_path
from .views import *
from Store.views import *
from app01.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('add_goods/', add_goods),
    path('orders/', orders),
    path('count_goods/', count_goods),
    path('count_orders/', count_orders),
    path('store/', store),
    path('add_info/', add_info),
    path('select_info/', select_info),



    re_path('computing_bir/(\d+)/(\d+)/',computing_bir)

]
