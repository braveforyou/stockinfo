#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import re, time, json, logging, hashlib, base64, asyncio
from aiohttp import web
from www.coroweb import get, post
from www.apis import Page, APIValueError, APIResourceNotFoundError
import stock.loadInfo.company.company as company

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


import pandas as pd
import numpy as np


@get('/')
def index(*, page='1'):
    print(page)
    num = 1
    page = Page(num)

    info = pd.read_csv("D:\\needStList.csv")
    info = np.array(info)

    content = []
    for i in range(len(info)):
        tempdict = {}
        tempdict['name'] = str(info[i][1])
        tempdict['refuseInfo'] = str(info[i][2])

        mc,yc=company.getCompanyInfo(info[i][1])

        tempdict['companyInfo_middleReport'] =mc
        tempdict['companyInfo_yearReport'] = yc
        content.append(tempdict)

    return {
        '__template__': 'stockinfo.html',
        'page': page,
        'blogs': content
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
