# coding=utf-8


import tushare as ts
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import www.config_default as config





''' 获取业绩报表数据 '''
def getAllFianceReport():
    needFinaceMonth = [[2019, 2], [2019, 1],
                       [2018, 4], [2018, 3], [2018, 2], [2018, 1],
                       [2017, 4], [2017, 3], [2017, 2], [2017, 1],
                       [2016, 4], [2016, 3], [2016, 2], [2016, 1]]
    for i in range(len(needFinaceMonth)):
        filename = "D:\\" + str(needFinaceMonth[i][0]) + str(needFinaceMonth[i][1]) + ".csv"
        report1 = ts.get_report_data(2019, 2)
        report1.to_csv(filename)
    return


# file3, file2, file1, 为当前周期， file32='', file22='', file12=''
# 为前者的前一周其，对于除第一周期外，需要得到当周期的实际数值就需要减去上一周其
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
        for i in range(len(midinfo)):
            midinfo[i, 1] = midinfo[i, 1] - midinfo2[i, 1]
            midinfo[i, 2] = midinfo[i, 2] - midinfo2[i, 2]
            midinfo[i, 3] = midinfo[i, 3] - midinfo2[i, 3]
        midinfo = pd.DataFrame(midinfo, columns=['code', 'eps3', 'eps2', 'eps1'])
    midinfo.to_csv('D:\\quertinfo' + str(quart) + '.csv')
    return list(np.array(midinfo['code']))

'''获取不同季度的信息的环比分析 '''
def Combine():
    list4 = analysisQuart('D:\\20184.csv', 'D:\\20174.csv', 'D:\\20164.csv', 'D:\\20183.csv', 'D:\\20173.csv',
                          'D:\\20163.csv', 4)
    list3 = analysisQuart('D:\\20183.csv', 'D:\\20173.csv', 'D:\\20163.csv', 'D:\\20182.csv', 'D:\\20172.csv',
                          'D:\\20162.csv', 3)
    list2 = analysisQuart('D:\\20192.csv', 'D:\\20182.csv', 'D:\\20172.csv', 'D:\\20191.csv', 'D:\\20181.csv',
                          'D:\\20171.csv', 2)
    list1 = analysisQuart('D:\\20191.csv', 'D:\\20181.csv', 'D:\\20171.csv', 1)

    combine = set(list2) & set(list1)
    return combine


def getCompanyInfo(stname):

    stname = int(str(stname).replace('st', ''))
    quart2 = pd.read_csv('D:\\quertinfo3.csv')[['code', 'eps3', 'eps2', 'eps1']]
    quart1 = pd.read_csv('D:\\quertinfo2.csv')[['code', 'eps3', 'eps2', 'eps1']]

    quart2 = quart2.loc[quart2['code'] == stname]
    quart1 = quart1.loc[quart1['code'] == stname]

    quart2 = np.array(quart2)
    quart1 = np.array(quart1)

    每股三季报收益详情 = ""
    每股中报收益详情 = ""

    三季报报每股收益下降 = 0  # 中保每股收益下降
    三季报收益各年 = [-1, -1, -1]
    rise1 = 0
    rise2 = 0
    if (len(quart2) != 0):
        每股三季报收益详情 = "三季报  每股收益:" + str(round(quart2[0][1], 2)) + "  " + str(round(quart2[0][2], 2)) + "  " + str(
            round(quart2[0][3], 2)) + " 近期增长:" + str(
            round((quart2[0][1] - quart2[0][2]) / quart2[0][2] * 100, 2)) + "% " + str(
            round((quart2[0][2] - quart2[0][3]) / quart2[0][3] * 100, 2)) + "%"
        三季报收益各年 = [quart2[0][1], quart2[0][2], quart2[0][3]]
        rise2 = round((quart2[0][1] - quart2[0][2]) / quart2[0][2] * 100, 2)
        if (quart2[0][1] < quart2[0][2]):
            三季报报每股收益下降 = -1
    if (len(quart1) != 0):
        每股中报收益详情 += "  中报 每股收益:" + str(round(quart1[0][1], 2)) + " " + str(round(quart1[0][2], 2)) + "  " + str(
            round(quart1[0][3], 2)) + " 近期增长:" + str(
            round((quart1[0][1] - quart1[0][2]) / quart1[0][2] * 100, 2)) + "% " + str(
            round((quart1[0][2] - quart1[0][3]) / quart1[0][3] * 100, 2)) + "%"
        rise1 = round((quart1[0][1] - quart1[0][2]) / quart1[0][2] * 100, 2)
    增速提高 = 0
    if (len(quart2) > 0 and len(quart1) > 0):
        增速提高 = 1 if rise2 - rise1 > 0 else 0

    return 每股三季报收益详情, 每股中报收益详情, 三季报报每股收益下降, 三季报收益各年, 增速提高

#    获取沪深上市公司基本情况
def getALLBaseInfo():
    allBase = ts.get_stock_basics()
    allBase.to_csv("D:\\allbase.csv")



def getBaseInfo(stname):
    stname = int(str(stname).replace('st', ''))
    alldata = pd.read_csv("D:\\allbase.csv")
    tempinfo = alldata.loc[alldata['code'] == stname]
    tempinfo = tempinfo[['code', 'name', 'industry', 'area', 'outstanding', 'totals', 'totalAssets', 'npr', 'esp']]
    tempinfo = np.array(tempinfo)[0]
    return list(tempinfo)


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



def getRonzi(stcode):
    url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?symbol=sh600702&bdate=2019-01-01&edate=2019-10-15'



if(config.init):
    getAllFianceReport()
    Combine()
    getALLBaseInfo()