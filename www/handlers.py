#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'


from www.old.apis import Page
import pandas as pd
import numpy as np
from flask_restful import Resource, reqparse
from www.response_vo import ResponseVo
from process.utils.TimeCostAnnotation import *
import process.services.stAnslysisService as stService
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
        result = index()
        json.dumps(obj=result)
        resp_vo = ResponseVo(success=True, data=result)
        return resp_vo.to_vo()

    # post提交时的处理方法
    def get(self):
        result = {}
        # 此种方法即可解析通过普通post提交也可解析json格式提交
        args = parser.parse_args()
        result["method"] = "post"
        result["q"] = args["q"]
        return result


@timerCost()
def index():
    num = 1
    page = Page(num)

    info = pd.read_csv("D:\\needStList.csv")
    info = np.array(info)

    content = []
    listNeed = []
    listFilter = []
    for i in range(len(info)):
        tempdict, needflag = stService.analysisInner(info[i][1])
        if (needflag == False):
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
