#-*- coding:utf-8 -*-
"""
@Time:2020/9/2620:15
@Auth:DaiXvWen
@File:render_to_render_tempalte.py
"""
from django.shortcuts import render

from .models import *#从app中导入数据库

class RenderWrite(object): #新建一个工具类
    def render_template(request, template_name, context=None, content_type=None, status=None, using=None):
        p_list = []
        c_list = []
        cate = models.OdooCategory.objects.all()
        for c in cate:
            data = {
                'name': c.name,
                'id': c.id
            }
            pro = models.OdooProducts.objects.filter(odoocategory=c.id)
            for p in pro:
                p_list.append(p)
            c_list.append(data)
        if isinstance(context, dict):
            context["c_list"] = c_list #需要的菜单列表
            context['p_list'] = p_list
        else:
            context = {
                "c_list": c_list,
                'p_list':p_list
            }
        return render(
            request=request,
            template_name=template_name,
            context=context,
            content_type=content_type,
            status=status,
            using=using
        )