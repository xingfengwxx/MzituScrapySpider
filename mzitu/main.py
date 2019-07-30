#!/usr/bin/env python 3.7
# -*- coding: utf-8 -*-
# @Time       : 2019/7/30 17:29
# @Author     : wangxingxing
# @Email      : xingfengwxx@gmail.com 
# @File       : main.py
# @Software   : PyCharm
# @Description: 

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl mzitu".split())