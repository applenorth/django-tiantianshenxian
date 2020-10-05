#-*- coding:utf-8 -*-
"""
@Time:2020/10/415:24
@Auth:DaiXvWen
@File:filters.py
"""
#store项目的自定义过滤器
#导入Library类
from django.template import Library


#实例化为对象，对象名称一定要是 register
register=Library()

#对象.filter函数装饰自定义的函数
#写自定义的函数解决问题，函数至少有一个形参
@register.filter
def goods_type_name(num):
    if num==1:
        return "Arknights"
    elif num==2:
        return "Genshin Impact"
    elif num==3:
        return "Azur Lane"
    elif num==4:
        return "Girls Frontline"
    elif num==5:
        return "Honkai Impact 3"
    else:
        return '没有找到'

