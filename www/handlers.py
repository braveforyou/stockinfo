#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'


from process.apis import Page
import pandas as pd
import numpy as np
from flask_restful import Resource, reqparse
from www.response_vo import ResponseVo
from process.utils.TimeCostAnnotation import *
import process.services.stAnslysisService as stService
import multiprocessing
from multiprocessing import Lock, Manager
import json

parser = reqparse.RequestParser()

'''
首先排序

而后则是既然是高价值的，那么更多的应该是长期投资，短期的做T后还要接回来

应该去普查基金持仓情况

股票相对强度，进一遍的涨幅
'''


class Rest(Resource):

    def post(self):
        result = indexParrel()
        json.dumps(obj=result)
        resp_vo = ResponseVo(success=True, data=result)
        return resp_vo.to_vo()

    def get(self):
        result = {}
        return result




def sort(content):
    tempList=[]
    for i in range(len(content)):
        tempList.append([content[i]['score'],i])
    tempList.sort(key=(lambda x:x[0]),reverse=True)
    index=np.array(tempList)[:,1]
    result=[]
    for x in index:
        result.append(content[int(x)])

    return result

@timerCost()
def indexParrel():
    num = 1
    page = Page(num)
    info = pd.read_csv("D:\\needStList.csv")
    info = np.array(info)

    manager = Manager()
    cpu_count = multiprocessing.cpu_count()
    lock = Lock()
    listFilter = manager.list()
    listNeed = manager.list()
    contents= manager.list()

    pool = multiprocessing.Pool(cpu_count, initializer=stService.initStParam,
                                initargs=(lock, listFilter, listNeed,contents,))
    pool.map(stService.analysisInner, info)
    contents=sort(contents)

    return {
        'page': page,
        'blogs': contents
    }





@timerCost()
def stSingle(stname):
    print(stname)
    stinfo=stService.analysisInnerInfo(stname)

    return {
        'stinfo': stinfo
    }

