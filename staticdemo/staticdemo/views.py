#-*- coding:utf-8 -*-
"""
@Time:2020/9/2316:21
@Auth:DaiXvWen
@File:views.py
"""
"""--------------------------------------视图文件---------------------------------------"""
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):

    return render_to_response("index.html")


def add_goods(request):

    return render_to_response("add_goods.html")

def orders(request):

    return render_to_response("orders.html")

def count_goods(request):

    return render_to_response("count_goods.html")

def count_orders(request):

    return render_to_response("count_orders.html")

def store(request):

    return render_to_response("store.html")

#作业计算生日
from datetime import *
def computing_bir(request,month,day):
    d1=datetime.strptime('2020/1/1','%Y/%m/%d')
    d2=datetime.strptime('2020'+'/{}/{}'.format(month,day),'%Y/%m/%d')
    days=(d2-d1).days+1

    return HttpResponse("你的生日是%s月%s日，是今年的第%s天" %(month,day,days))

