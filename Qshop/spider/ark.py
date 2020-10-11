#-*- coding:utf-8 -*-
"""
@Time:2020/10/922:12
@Auth:DaiXvWen
@File:bilibili.py
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
def parse_page(html_str):
    '''
    解析页面，获取单词
    :param html_str:
    :return:
    '''
    #第一步：将字符串编程element对象
    tree = etree.HTML(html_str)
    # print(tree)
    print(html_str)
def main():
    ua = UserAgent()
    # print(ua.random)
    #确定url
    base_url = 'https://ak.hypergryph.com/index'
    headers= {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    response = requests.get(base_url,headers = headers)

    parse_page(response.text)



if __name__ == '__main__':
    main()