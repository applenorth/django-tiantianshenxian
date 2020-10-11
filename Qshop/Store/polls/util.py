#-*- coding:utf-8 -*-
"""
@Time:2020/10/815:23
@Auth:DaiXvWen
@File:util.py
"""
import random
def gen_verify_code(length = 4):
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    return ''.join(random.choices(all_chars,k = length))
