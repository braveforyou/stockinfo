#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import re
from www.apis import Page
import process.loadInfo.company.company as company
import pandas as pd
import numpy as np
from flask_restful import Resource, reqparse
from www.response_vo import ResponseVo
parser = reqparse.RequestParser()
import json
'''
首先排序

而后则是既然是高价值的，那么更多的应该是长期投资，短期的做T后还要接回来

应该去普查基金持仓情况

股票相对强度，进一遍的涨幅
'''


class Rest(Resource):
    # get提交时的处理方法
    def post(self):
        info = pd.read_csv("D:\\needStList.csv")
        info = np.array(info)

        content = []
        listNeed = []
        listFilter = []
        for i in range(len(info)):

            if(i>20):break
            if (i % 10 == 0):
                print(i)
            tempdict = {}
            tempdict['name'] = str(info[i][1])

            每股中报收益详情, 每股一季度报收益详情, 中报每股收益下降, 中报收益各年, 增速提高 = company.getCompanyInfo(info[i][1])

            tempdict['companyInfo_middleMeiGuReport'] = 每股中报收益详情
            tempdict['companyInfo_oneQuartMeiGuReport'] = 每股一季度报收益详情

            baseinfo = company.getBaseInfo(info[i][1])
            stnamex = str(baseinfo[0])
            if (len(stnamex) != 6):
                for i in range(6 - len(stnamex)):
                    stnamex = '0' + stnamex
                stnamex = 'sz' + stnamex
            else:
                stnamex = 'sh' + stnamex

            baseinfo[0] = stnamex

            tabelShow = []
            tabelShow.append(中报每股收益下降)  # 每股收益下降w
            tabelShow = [float(x) for x in tabelShow]
            tabelShow.append(增速提高)  # 每股收益下降w
            # if(中报收益各年[0]<0 and 中报收益各年[0]!=-100):continue#进一季度的每股收益率

            sallaryPerSt = baseinfo[-1]  # 每股价格
            stname = info[i][1].replace('st', '')
            priceNow = pd.read_csv("D:\PythonTrain\stockListNow\\" + stname + ".csv")
            priceLatest = np.array(priceNow)[0, 3]
            priceMax = np.max(np.array(priceNow)[:, 3])
            priceNow = np.array(priceNow)[-1, 3]

            expectSallary100 = sallaryPerSt * 100 / priceNow
            gonggao = company.getCompanyGonGao(stname)

            jiejing = 0
            xianshou = -1
            zengchi = 0
            if (len(gonggao) > 0):
                for i in range(len(gonggao)):
                    if (gonggao[i][1].find('解禁')):
                        jiejing = -1
                    if (gonggao[i][1].find('限售')):
                        xianshou = -1
                    if (gonggao[i][1].find('增持')):
                        zengchi = 1
            tabelShow.append(jiejing)  # 解禁
            tabelShow.append(xianshou)  # 限售
            tabelShow.append(zengchi)

            tempdict['refuseInfo'] = tabelShow
            tempdict['score'] = sum(tabelShow)
            tempdict['baseinfo'] = baseinfo
            tempdict['expectSallary100'] = round(expectSallary100)
            tempdict['reportInfo'] = gonggao

            tempdict['currentrise'] = round((priceNow - priceLatest) / priceLatest * 100, 2)
            tempdict['maxrise'] = round((priceMax - priceLatest) / priceLatest * 100, 2)
            tempdict['currentPrice'] = round(priceNow, 2)

            if (中报收益各年[0] < 0 and 中报收益各年[0] != -100 or tempdict['currentrise'] < 10):
                listFilter.append(tempdict['currentrise'])
                continue
            else:
                listNeed.append(tempdict['currentrise'])
            content.append(tempdict)
        print('need:', np.mean(listNeed), np.max(listNeed), np.min(listNeed), np.median(listNeed))
        print('filter:', np.mean(listFilter), np.max(listFilter), np.min(listFilter), np.median(listFilter))

        result = {'page':1,'blogs': content}
        json.dumps(obj=result)
        resp_vo = ResponseVo(success=True, data=result)
        return  resp_vo.to_vo()

    # post提交时的处理方法
    def get(self):
        result = {}
        # 此种方法即可解析通过普通post提交也可解析json格式提交
        args = parser.parse_args()
        result["method"] = "post"
        result["q"] = args["q"]
        return result


def index(*, page='1'):
    num = 1
    page = Page(num)

    info = pd.read_csv("D:\\needStList.csv")
    info = np.array(info)

    content = []
    listNeed = []
    listFilter = []
    for i in range(len(info)):
        if (i % 10 == 0):
            print(i)
        tempdict = {}
        tempdict['name'] = str(info[i][1])

        每股中报收益详情, 每股一季度报收益详情, 中报每股收益下降, 中报收益各年, 增速提高 = company.getCompanyInfo(info[i][1])

        tempdict['companyInfo_middleMeiGuReport'] = 每股中报收益详情
        tempdict['companyInfo_oneQuartMeiGuReport'] = 每股一季度报收益详情

        baseinfo = company.getBaseInfo(info[i][1])
        stnamex = str(baseinfo[0])
        if (len(stnamex) != 6):
            for i in range(6 - len(stnamex)):
                stnamex = '0' + stnamex
            stnamex = 'sz' + stnamex
        else:
            stnamex = 'sh' + stnamex

        baseinfo[0] = stnamex

        tabelShow = []
        tabelShow.append(中报每股收益下降)  # 每股收益下降w
        tabelShow = [float(x) for x in tabelShow]
        tabelShow.append(增速提高)  # 每股收益下降w
        # if(中报收益各年[0]<0 and 中报收益各年[0]!=-100):continue#进一季度的每股收益率

        sallaryPerSt = baseinfo[-1]  # 每股价格
        stname = info[i][1].replace('st', '')
        priceNow = pd.read_csv("D:\PythonTrain\stockListNow\\" + stname + ".csv")
        priceLatest = np.array(priceNow)[0, 3]
        priceMax = np.max(np.array(priceNow)[:, 3])
        priceNow = np.array(priceNow)[-1, 3]

        expectSallary100 = sallaryPerSt * 100 / priceNow
        gonggao = company.getCompanyGonGao(stname)

        jiejing = 0
        xianshou = -1
        zengchi = 0
        if (len(gonggao) > 0):
            for i in range(len(gonggao)):
                if (gonggao[i][1].find('解禁')):
                    jiejing = -1
                if (gonggao[i][1].find('限售')):
                    xianshou = -1
                if (gonggao[i][1].find('增持')):
                    zengchi = 1
        tabelShow.append(jiejing)  # 解禁
        tabelShow.append(xianshou)  # 限售
        tabelShow.append(zengchi)

        tempdict['refuseInfo'] = tabelShow
        tempdict['score'] = sum(tabelShow)
        tempdict['baseinfo'] = baseinfo
        tempdict['expectSallary100'] = round(expectSallary100)
        tempdict['reportInfo'] = gonggao

        tempdict['currentrise'] = round((priceNow - priceLatest) / priceLatest * 100, 2)
        tempdict['maxrise'] = round((priceMax - priceLatest) / priceLatest * 100, 2)
        tempdict['currentPrice'] = round(priceNow, 2)

        if (中报收益各年[0] < 0 and 中报收益各年[0] != -100 or tempdict['currentrise'] < 10):
            listFilter.append(tempdict['currentrise'])
            continue
        else:
            listNeed.append(tempdict['currentrise'])
        content.append(tempdict)
    print('need:', np.mean(listNeed), np.max(listNeed), np.min(listNeed), np.median(listNeed))
    print('filter:', np.mean(listFilter), np.max(listFilter), np.min(listFilter), np.median(listFilter))

    return {
        'page': page,
        'blogs': content
    }
