#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''


class Stock():
    __table__ = 'blogs'
    id = 0
    name = ''
    price = 0
    priceinfo = ''  # 价格信息
    companyInfo = ''  # 公司盈利信息
    reportInfo = ''  # 公告信息
