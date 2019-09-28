#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import numpy as np
from pandas import DataFrame
from multiprocessing.dummy import Pool as ThreadPool
import datetime


# 获取历史信息
def getHistoryStockInfo(url):
    """根据url获取信息"""
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    stockStr = response.read().decode('gbk')
    stockList = stockStr.split('\\n\\')

    stockList = [x.replace('\n', '').replace("\";", '') for x in stockList]

    stockList = [x.split(" ") for i, x in enumerate(stockList) if i != 0 and i < len(stockList) - 1]
    stockList = np.array(stockList)

    return stockList


# http://data.gtimg.cn/flashdata/hushen/weekly/sh600198.js
# http://data.gtimg.cn/flashdata/hushen/daily/13/sz000750.js
# 拼接网址
def getHistory(year, code):
    """根据代码获取详细的url"""
    if (year < 10):
        yearhtm = '0' + str(year)
    else:
        yearhtm = str(year)
    if (code[0] == '6'):
        url = 'http://data.gtimg.cn/flashdata/hushen/monthly/'
        url += 'sh' + str(code) + '.js'
    else:
        url = 'http://data.gtimg.cn/flashdata/hushen/monthly/'
        url += 'sz' + str(code) + '.js'

    return url


# 获取时间段内的历史记录
def getHistoryFile(code, begain=16, end=19):
    temp = []
    for i in range(begain, end + 1):
        url = getHistory(i, code)
        try:
            stockList = getHistoryStockInfo(url)
        except:
            continue
        if (i == begain):
            temp = stockList
        else:
            temp = np.vstack((stockList, temp))
    column = ['data', 'open', 'close', 'high', 'bottom', 'amount']
    filename = "D:\PythonTrain\stockListM\\" + str(code) + ".csv"
    print(filename)
    if(len(temp)>200):
        temp = temp[temp[:, 0].argsort()][-200:]

    DataFrame(temp, columns=column).to_csv(filename)
    return


import stock.model.consts as consts

SuccessList = []

countx = [0]


def getinfo(stockname):
    # 时间 开盘 收盘  最高 最低 成交量
    try:
        print(countx[0])
        countx[0] += 1
        getHistoryFile(stockname)
    except:
        raise
        1


def getstockinfoList(stocklist):
    pool2 = ThreadPool(12)
    pool2.map(getinfo, stocklist)
    return 0;


def main():
    a = datetime.datetime.now()
    listtrain = consts.needStockMf1
    print(listtrain)
    getstockinfoList(listtrain)
    d = datetime.datetime.now()
    print("process end in ", (d - a).seconds)
    print(SuccessList)
