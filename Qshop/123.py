#-*- coding:utf-8 -*-
"""
@Time:2020/9/309:15
@Auth:DaiXvWen
@File:123.py
"""
a=None
if a:
    print('success')

if a is None:
    print('a是none，是空值')

if a is not None:
    print('a不是空值')
b=2
print(id(b))
