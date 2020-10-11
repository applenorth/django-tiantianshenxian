#-*- coding:utf-8 -*-
"""
@Time:2020/10/716:15
@Auth:DaiXvWen
@File:面向对象.py
"""
class Animal:
    pass
class Xxx:
    pass

class Dog(Animal,Xxx):
    pass

d=Dog()
print(type(d))
print(d.__class__)
print(type(Dog))
print(Dog.__class__)
print(int.__class__)
print(int.__base__)
print(float.__class__)
print(bool.__class__)
print(object.__class__)
print(object.__base__)
print(type.__base__)