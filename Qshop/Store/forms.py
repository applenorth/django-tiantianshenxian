#-*- coding:utf-8 -*-
"""
@Time:2020/9/2716:04
@Auth:DaiXvWen
@File:form.py
"""
from django import forms
from django.core.validators import RegexValidator,EmailValidator
from django.core.exceptions import ValidationError
from .models import *
#自定义过滤器

#一：函数的方法
def checkusername(values):
    """
    # 校验账号中不能包含铭感
    :param values:   获取到的数据
    :return:    抛出异常
    """
    data_list=['sb','admin']
    for one in data_list:
        if one in values:
            #不通过，抛出异常
            raise ValidationError('账号中不能包含铭感词汇')


#二：类方法
class CheckUsername():
    #重写call方法
    def __call__(self, value):
        data_list = ['sb', 'admin']
        for one in data_list:
            if one in value:
                # 不通过，抛出异常
                raise ValidationError('账号中不能包含铭感词汇')

#自定义注册校验，检验账号是否重复，密码是否一致，密码是否填写
class CheckG():
    def checkusername(username):
    #重写call方法
        username1=QUser.objects.filter(username=username)
        if username1:
            #不通过，抛出异常
            raise ValidationError('账号已存在，请换个账号名')
#登录校验
class UserLogin(forms.Form):
    username = forms.CharField(
        error_messages={"required": "请填写账号名"}
    )
    password = forms.CharField(
        error_messages={"required": "请填写密码"}
    )

#注册校验
class RegisterUser(forms.Form):

    username=forms.CharField(
        validators=[
            CheckG.checkusername
        ],
        error_messages={"required": "必填"}
    )

# 编写后端用户中心校验规则
class PersonForm(forms.Form):
    #昵称校验
    nick_name=forms.CharField(
        error_messages={"required":"必填"}
    )

    #手机号码校验
    phone = forms.CharField(
        validators=[
            RegexValidator("^1[35678]\d{9}$", message="请填入正确的手机号")
        ],
        error_messages={"required": "必填"}
    )

    #邮箱校验
    email=forms.CharField(
        validators=[
            EmailValidator(message="必须为邮箱格式")
        ],
        error_messages={"required":"必填"}

    )

    #地址校验
    address=forms.CharField(
        error_messages={"required":"必填"}
    )
