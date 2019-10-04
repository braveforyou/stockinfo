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
import tushare as ts


@get('/')
def index(*, page='1'):
    num = 1
    page = Page(num)

    info = pd.read_csv("D:\\needStList.csv")
    info = np.array(info)

    content = []
    for i in range(len(info)):
        tempdict = {}
        tempdict['name'] = str(info[i][1])

        meiguMid, oneMInfo, meiGuDecress, meiGuDecress2, zbsy = company.getCompanyInfo(info[i][1])


        tempdict['companyInfo_middleMeiGuReport'] = meiguMid
        tempdict['companyInfo_oneQuartMeiGuReport'] = oneMInfo

        baseinfo = company.getBaseInfo(info[i][1])

        temp = info[i][2]
        temp = temp.replace('[', '').replace(']', '')
        temp = temp.split(',')
        temp.append(meiGuDecress)
        temp.append(meiGuDecress2)
        temp = [float(x) for x in temp]

        if(zbsy[0]<0 and zbsy[0]!=-100):continue#进一季度的每股收益率



        sallaryPerSt = baseinfo[-1]  # 每股价格
        stname = info[i][1].replace('st', '')
        priceNow = pd.read_csv("D:\PythonTrain\stockListNow\\" + stname + ".csv")
        priceLatest = np.array(priceNow)[0, 3]
        priceMax = np.max(np.array(priceNow)[:, 3])
        priceNow = np.array(priceNow)[-1, 3]

        expectSallary100 = sallaryPerSt * 100 / priceNow
        gonggao=company.getCompanyGonGao(stname)

        jiejing=0
        xianshou=-1
        if(len(gonggao)>0):
            for i in range(len(gonggao)):
                if(gonggao[i][1].find('解禁')):
                    jiejing=-1
                if (gonggao[i][1].find('限售')):
                    xianshou = -1
        temp.append(jiejing)
        temp.append(xianshou)


        tempdict['refuseInfo'] = temp
        tempdict['score'] = sum(temp)
        tempdict['baseinfo'] = baseinfo
        tempdict['expectSallary100'] = round(expectSallary100)
        tempdict['reportInfo'] = gonggao

        tempdict['currentrise'] = round((priceNow - priceLatest) / priceLatest * 100, 2)
        tempdict['maxrise'] = round((priceMax - priceLatest) / priceLatest * 100, 2)
        tempdict['currentPrice'] = round(priceNow, 2)
        content.append(tempdict)

    return {
        '__template__': 'stockinfo.html',
        'page': page,
        'blogs': content
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
