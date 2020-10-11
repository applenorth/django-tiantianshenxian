#-*- coding:utf-8 -*-
"""
@Time:2020/10/916:42
@Auth:DaiXvWen
@File:MyMiddleWare.py
"""
#中间件处理
from django.utils.deprecation import MiddlewareMixin

class MyMiddWareTest(MiddlewareMixin):
    def process_request(self, request):
        print("md1  process_request 方法。", id(request))  # 在视图之前执行

    def process_response(self, request, response):# 基于请求响应

        print("md1  process_response 方法！", id(request))  # 在视图之后
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("md1  process_view 方法！")  # 在视图之前执行 顺序执行
        # return view_func(request)

    def process_exception(self, request, exception):  # 引发错误 才会触发这个方法
        print("md1  process_exception 方法！")
        # return HttpResponse(exception) #返回错误信息