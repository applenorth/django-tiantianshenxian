from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
#json与ajax测试，返回一个json格式的用户信息
from django.http import JsonResponse
# Create your views here.

#首页
def index(request):

    return render(request,'buyer/index.html',locals())

#登录
def login(request):

    return render(request,'buyer/login.html',locals())

#注册
def register(request):

    return render(request,'buyer/register.html',locals())

#购物车
def cart(request):

    return render(request,'buyer/cart.html',locals())


##修改购物地址
def edit_address(request):

    return render(request,'buyer/edit-address.html',locals())

##修改用户信息
def edit_user(request):

    return render(request,'buyer/edit-user.html',locals())


##我的订单
def myorders(request):

    return render(request,'buyer/myorders.html',locals())

##提交订单
def place_order(request):

    return render(request,'buyer/place_order.html',locals())

#用户中心个人信息
def usercenterinfo(request):

    return render(request,'buyer/user-center-info.html',locals())


#list界面
def list(request):

    return render(request,'buyer/list.html',locals())