#-*- coding:utf-8 -*-
"""
@Time:2020/9/2216:35
@Auth:DaiXvWen
@File:views.py
"""
"""---------------------------------视图文件----------------------------------"""
from django.http import HttpResponse
def index(request):
    """
    视图函数：接收用户的请求，处理请求，返回响应
    :param request: 包含请求信息的请求对象
    :return: 返回一个响应对象
    """


    return HttpResponse("hello world")

def test1(request,year,name1,city,name2):


    return HttpResponse("%s年%s在%s城市，暴打了%s" %(year,name1,city,name2))

#首页页面调用
from django.shortcuts import render_to_response
# def index1(request):  #必须填写request
#
#     parmas={
#         "name":"李嗨涛",
#         "age":18,
#         "gender":"男"
#     }
#
#     #django收集的变量就是字典，因此不需要解包，直接使用locals传参
#     return render_to_response("demo.html",parmas)

def index1(request):  #必须填写request

    name="李嗨涛"
    age=12
    gender="男"
    hobby=["抽烟","喝酒","烫头"]
    score={
        "python":100,
        "java":80,
        "linux":60
    }
    #django收集的变量就是字典，因此不需要解包，直接使用locals传参
    return render_to_response("demo.html",locals())

def demo1(request):

    return render_to_response("demo1.html")

def demo2(request):
    return render_to_response("demo2.html")


def demo3(request):
    return render_to_response("demo3.html")