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
    report2 = ts.get_report_data(2019, 1)
    report2.to_csv('D:\\20191.csv')
    report3 = ts.get_report_data(2018, 4)
    report3.to_csv('D:\\20184.csv')
    report4 = ts.get_report_data(2018, 3)
    report4.to_csv('D:\\20183.csv')
    report5 = ts.get_report_data(2018, 2)
    report5.to_csv('D:\\20182.csv')
    report6 = ts.get_report_data(2018, 1)
    report6.to_csv('D:\\20181.csv')
    report7 = ts.get_report_data(2017, 4)
    report7.to_csv('D:\\20174.csv')
    report8 = ts.get_report_data(2017, 3)
    report8.to_csv('D:\\20173.csv')
    report9 = ts.get_report_data(2017, 2)
    report9.to_csv('D:\\20172.csv')
    report10 = ts.get_report_data(2017, 1)
    report10.to_csv('D:\\20171.csv')
    report11 = ts.get_report_data(2016, 4)
    report11.to_csv('D:\\20164.csv')
    report12 = ts.get_report_data(2016, 3)
    report12.to_csv('D:\\20163.csv')
    report12 = ts.get_report_data(2016, 2)
    report12.to_csv('D:\\20162.csv')
    report12 = ts.get_report_data(2016, 1)
    report12.to_csv('D:\\20161.csv')
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


# file3, file2, file1, 为当前周期， file32='', file22='', file12='' 为前者的前一周其，对于除第一周期外，需要得到当周期的实际数值就需要减去上一周其
def analysisQuart(file3, file2, file1, file32='', file22='', file12='', quart=1):
    data3 = pd.read_csv(file3)[['code', 'eps']]
    data2 = pd.read_csv(file2)[['code', 'eps']]
    data1 = pd.read_csv(file1)[['code', 'eps']]

    data3 = data3.rename(columns={'eps': 'eps3'})
    data2 = data2.rename(columns={'eps': 'eps2'})
    data1 = data1.rename(columns={'eps': 'eps1'})

    midinfo = pd.merge(data3, data2, on=['code'], how='inner')

    midinfo = pd.merge(midinfo, data1, on=['code'], how='inner')
    midinfo = midinfo[['code', 'eps3', 'eps2', 'eps1']]

    midinfo2 = []
    if (quart != 1):
        data32 = pd.read_csv(file32)[['code', 'eps']]
        data22 = pd.read_csv(file22)[['code', 'eps']]
        data12 = pd.read_csv(file12)[['code', 'eps']]

        data32 = data32.rename(columns={'eps': 'eps3'})
        data22 = data22.rename(columns={'eps': 'eps2'})
        data12 = data12.rename(columns={'eps': 'eps1'})

        midinfo2 = pd.merge(data32, data22, on=['code'], how='left')

        midinfo2 = pd.merge(midinfo2, data12, on=['code'], how='left')
        midinfo2 = midinfo2[['code', 'eps3', 'eps2', 'eps1']]

    if (len(midinfo2) != 0):
        midinfo2 = np.array(midinfo2)
        midinfo = np.array(midinfo)
        print(len(midinfo), '---', len(midinfo2))
        for i in range(len(midinfo)):
            midinfo[i, 1] = midinfo[i, 1] - midinfo2[i, 1]
            midinfo[i, 2] = midinfo[i, 2] - midinfo2[i, 2]
            midinfo[i, 3] = midinfo[i, 3] - midinfo2[i, 3]
        midinfo = pd.DataFrame(midinfo, columns=['code', 'eps3', 'eps2', 'eps1'])
    midinfo.to_csv('D:\\quertinfo' + str(quart) + '.csv')
    return list(np.array(midinfo['code']))


def Combine():
    list4 = analysisQuart('D:\\20184.csv', 'D:\\20174.csv', 'D:\\20164.csv', 'D:\\20183.csv', 'D:\\20173.csv',
                          'D:\\20163.csv', 4)
    list3 = analysisQuart('D:\\20183.csv', 'D:\\20173.csv', 'D:\\20163.csv', 'D:\\20182.csv', 'D:\\20172.csv',
                          'D:\\20162.csv', 3)
    list2 = analysisQuart('D:\\20192.csv', 'D:\\20182.csv', 'D:\\20172.csv', 'D:\\20191.csv', 'D:\\20181.csv',
                          'D:\\20171.csv', 2)
    list1 = analysisQuart('D:\\20191.csv', 'D:\\20181.csv', 'D:\\20171.csv', 1)

    combine = set(list2) & set(list1)
    print(combine)


# getAllFiance()
# Combine()


def getCompanyInfo(stname):
    stname = int(stname.replace('st', ''))
    quart2 = pd.read_csv('D:\\quertinfo2.csv')[['code', 'eps3', 'eps2', 'eps1']]
    quart1 = pd.read_csv('D:\\quertinfo1.csv')[['code', 'eps3', 'eps2', 'eps1']]

    quart2 = quart2.loc[quart2['code'] == stname]
    quart1 = quart1.loc[quart1['code'] == stname]

    quart2 = np.array(quart2)
    quart1 = np.array(quart1)

    meiguMid = ""
    oneMInfo = ""

    meiGuDecress = 0
    meiGuDecress2 = 0
    zbsy = [-1, -1, -1]
    if (len(quart2) != 0):
        meiguMid = "中报  每股收益:" + str(round(quart2[0][1], 2)) + "  " + str(round(quart2[0][2], 2)) + "  " + str(
            round(quart2[0][3], 2)) + " 近期增长:" + str(
            round((quart2[0][1] - quart2[0][2]) / quart2[0][2] * 100, 2)) + "% " + str(
            round((quart2[0][2] - quart2[0][3]) / quart2[0][3] * 100, 2)) + "%"
        zbsy = [quart2[0][1], quart2[0][2], quart2[0][3]]
        if (quart2[0][1] < quart2[0][2]):
            meiGuDecress = -1
    if (len(quart1) != 0):
        oneMInfo += "  一季报 每股收益:" + str(round(quart1[0][1], 2)) + " " + str(round(quart1[0][2], 2)) + "  " + str(
            round(quart1[0][3], 2)) + " 近期增长:" + str(
            round((quart1[0][1] - quart1[0][2]) / quart1[0][2] * 100, 2)) + "% " + str(
            round((quart1[0][2] - quart1[0][3]) / quart1[0][3] * 100, 2)) + "%"

    return meiguMid, oneMInfo, meiGuDecress, meiGuDecress2, zbsy


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
    alldata = pd.read_csv("D:\\allbase.csv")
    tempinfo = alldata.loc[alldata['code'] == stname]
    tempinfo = tempinfo[['code', 'name', 'industry', 'area', 'outstanding', 'totals', 'totalAssets', 'npr', 'esp']]

    tempinfo = np.array(tempinfo)[0]

    return list(tempinfo)


# getALLBaseInfo()
import requests


def getCompanyGonGao(stcode):

    url = 'http://www.tou18.cn/gonggao/' + str(stcode)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    reponse = requests.get(url)
    reponse.encoding = 'GBK'
    soup = BeautifulSoup(reponse.content)
    test = soup.find_all('div', class_='table1')
    result = []
    count = 0
    for k in test:
        for item in k.find_all('tr'):
            count += 1
            if (count > 10): continue
            temp = []
            for inner in item:
                temp.append(inner.text)
            result.append(temp)
    return result

