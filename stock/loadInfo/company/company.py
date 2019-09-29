# coding=utf-8
from html.parser import HTMLParser

import sys

type = sys.getfilesystemencoding()

import tushare as ts
from lxml import html
import stock.baseinfo.HttpUtil as httpUtil
from bs4 import BeautifulSoup


def analysis(sallary):
    riseAll = []
    for i in range(4):
        rise1 = (sallary[i] - sallary[i + 4]) / sallary[i + 4] * 100
        rise2 = (sallary[i + 4] - sallary[i + 8]) / sallary[i + 8] * 100
        rise3 = (sallary[i + 8] - sallary[i + 12]) / sallary[i + 12] * 100
        riseAll.append([round(rise1, 2), round(rise2, 2), round(rise3, 2)])
    return riseAll


def getAllFiance():
    report1 = ts.get_report_data(2019, 2)
    report1.to_csv('D:\\20192.csv')

    '''
    report2 = ts.get_report_data(2019,1)
    report2.to_csv('D:\\20191.csv')
    report3 = ts.get_report_data(2018,4)
    report3.to_csv('D:\\20184.csv')
    report4 = ts.get_report_data(2018,3)
    report4.to_csv('D:\\20183.csv')
    report5 = ts.get_report_data(2018,2)
    report5.to_csv('D:\\20182.csv')
    report6 = ts.get_report_data(2018,1)
    report6.to_csv('D:\\20181.csv')
    report7 = ts.get_report_data(2017,4)
    report7.to_csv('D:\\20174.csv')
    report8 = ts.get_report_data(2017,3)
    report8.to_csv('D:\\20173.csv')
    report9 = ts.get_report_data(2017,2)
    report9.to_csv('D:\\20172.csv')
    report10 = ts.get_report_data(2017,1)
    report10.to_csv('D:\\20171.csv')
    report11 = ts.get_report_data(2016,4)
    report11.to_csv('D:\\20164.csv')
    report12 = ts.get_report_data(2016,3)
    report12.to_csv('D:\\20163.csv')
    '''

    return


'''
code,代码
name,名称
esp,每股收益
eps_yoy,每股收益同比(%)
bvps,每股净资产
roe,净资产收益率(%)
epcf,每股现金流量(元)
net_profits,净利润(万元)
profits_yoy,净利润同比(%)
distrib,分配方案
report_date,发布日期
'''
import numpy as np
import pandas as pd


def getstname(st):
    st = int(st)
    st = str(st)
    if (len(st) == 1):
        st = '00000' + st
    elif (len(st) == 2):
        st = '0000' + st
    elif (len(st) == 3):
        st = '000' + st
    elif (len(st) == 4):
        st = '00' + st
    elif (len(st) == 5):
        st = '0' + st
    return st


def Combine():
    mid201902 = pd.read_csv('D:\\20192.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]
    mid201902 = mid201902.loc[mid201902['net_profits'] > 0]
    mid201802 = pd.read_csv('D:\\20182.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]
    mid01702 = pd.read_csv('D:\\20172.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]

    mid201902 = mid201902.rename(columns={'profits_yoy': 'profits_yoy3'})
    mid201802 = mid201802.rename(columns={'profits_yoy': 'profits_yoy2'})
    mid01702 = mid01702.rename(columns={'profits_yoy': 'profits_yoy1'})

    mid201902 = mid201902.rename(columns={'eps_yoy': 'eps_yoy3'})
    mid201802 = mid201802.rename(columns={'eps_yoy': 'eps_yoy2'})
    mid01702 = mid01702.rename(columns={'eps_yoy': 'eps_yoy1'})

    midinfo = pd.merge(mid201902, mid201802, on=['code'], how='left')
    midinfo = pd.merge(midinfo, mid01702, on=['code'], how='left')

    year201902 = pd.read_csv('D:\\20184.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]
    year201802 = pd.read_csv('D:\\20174.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]
    year201702 = pd.read_csv('D:\\20164.csv')[['code', 'roe', 'eps_yoy', 'net_profits', 'profits_yoy']]
    year201902 = year201902.loc[year201902['net_profits'] > 0]

    year201902 = year201902.rename(columns={'profits_yoy': 'profits_yoy3'})
    year201802 = year201802.rename(columns={'profits_yoy': 'profits_yoy2'})
    year201702 = year201702.rename(columns={'profits_yoy': 'profits_yoy1'})

    year201902 = year201902.rename(columns={'eps_yoy': 'eps_yoy3'})
    year201802 = year201802.rename(columns={'eps_yoy': 'eps_yoy2'})
    year201702 = year201702.rename(columns={'eps_yoy': 'eps_yoy1'})

    yearinfo = pd.merge(year201902, year201802, on=['code'], how='left')
    yearinfo = pd.merge(yearinfo, year201702, on=['code'], how='left')

    midinfo = midinfo[['code', 'profits_yoy3', 'profits_yoy2', 'profits_yoy1', 'eps_yoy3', 'eps_yoy2', 'eps_yoy1']]
    midinfo = midinfo.loc[midinfo['profits_yoy3'] > 0]
    midinfo = midinfo.loc[midinfo['profits_yoy2'] > 0]
    midinfo = midinfo.drop_duplicates(subset=['code'], keep='first')

    midinfo.to_csv('D:\\midinfo.csv')
    stlist = list(np.array(midinfo['code']))

    # 分别是
    yearinfo = yearinfo[['code', 'profits_yoy3', 'profits_yoy2', 'profits_yoy1', 'eps_yoy3', 'eps_yoy2', 'eps_yoy1']]
    yearinfo = yearinfo.loc[yearinfo['profits_yoy3'] > 0]
    yearinfo = yearinfo.loc[yearinfo['profits_yoy2'] > 0]
    yearinfo = yearinfo.drop_duplicates(subset=['code'], keep='first')

    yearinfo.to_csv('D:\\yearinfo.csv')

    stlist2 = list(np.array(yearinfo['code']))
    combine = set(stlist) & set(stlist2)

    needList = []
    midinfo = np.array(midinfo[['code', 'profits_yoy3', 'profits_yoy2']])
    for i in range(len(midinfo)):
        if (midinfo[i, 0] in list(combine)):
            if (midinfo[i, 1] >= midinfo[i, 2]):
                needList.append(getstname(midinfo[i, 0]))


# Combine()


def getCompanyInfo(stname):
    stname = int(stname.replace('st', ''))
    midinfo = pd.read_csv('D:\\midinfo.csv')[
        ['code', 'profits_yoy3', 'profits_yoy2', 'profits_yoy1', 'eps_yoy3', 'eps_yoy2', 'eps_yoy1']]
    yearinfo = pd.read_csv('D:\\yearinfo.csv')[
        ['code', 'profits_yoy3', 'profits_yoy2', 'profits_yoy1', 'eps_yoy3', 'eps_yoy2', 'eps_yoy1']]

    midinfo = midinfo.loc[midinfo['code'] == stname]
    yearinfo = yearinfo.loc[yearinfo['code'] == stname]

    midinfo = np.array(midinfo)
    yearinfo = np.array(yearinfo)
    mcontent = ""
    yearcontent = ""
    meiguMid = ""
    meiguYear = ""

    meiGuDecress = 0
    meiGuDecress2 = 0
    if (len(midinfo) != 0):
        mcontent = "中报 增长率:" + str(midinfo[0][1]) + "%  " + str(midinfo[0][2]) + "%  " + str(midinfo[0][3]) + "%"
        meiguMid = "中报  每股收益率:" + str(midinfo[0][4]) + "%  " + str(midinfo[0][5]) + "%  " + str(midinfo[0][6]) + "%"
    if (len(yearinfo) != 0):
        yearcontent += "  年报 增长率:" + str(yearinfo[0][1]) + "%  " + \
                       str(yearinfo[0][2]) + "%  " + str(yearinfo[0][3]) + "%"
        meiguYear += "  年报 每股收益率:" + str(yearinfo[0][4]) + "%  " + \
                     str(yearinfo[0][5]) + "%  " + str(yearinfo[0][6]) + "%"
        if (yearinfo[0][4] < yearinfo[0][5]):
            meiGuDecress = -1
        if (yearinfo[0][4] < 0):
            meiGuDecress2 = -5

    return mcontent, yearcontent, meiguMid, meiguYear, meiGuDecress, meiGuDecress2


'''
code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
npr,净利润率(%)
   '''

def getALLBaseInfo():
    allBase = ts.get_stock_basics()

    allBase.to_csv("D:\\allbase.csv")

def getBaseInfo(stname):
    stname = int(stname.replace('st', ''))
    alldata=pd.read_csv("D:\\allbase.csv")
    tempinfo = alldata.loc[alldata['code'] == stname]
    tempinfo=tempinfo[['code','name','industry','area','outstanding','totals','totalAssets','npr']]

    tempinfo=np.array(tempinfo)[0]

    return list(tempinfo)
