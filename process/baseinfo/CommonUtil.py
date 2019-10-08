from numpy import *
import base64
import os
import hashlib
import gzip
import json, gzip



# 将list转换为频率词典
def getdic(list1):
    dic1 = {}
    # 统计accounts出现的次数
    for i in range(len(list1)):
        if (dic1.get(list1[i]) == None):
            dic1[list1[i]] = 1
        else:
            dic1[list1[i]] += 1
    keys = tuple(dic1.keys())
    return dic1, keys


# 字典排序 0按照key  1按照值 reverse=false 升序  reverse=true 降序
def sort_by_value(inputdic, choice=0, reverse=False):
    return sorted(inputdic.items(), key=lambda x: x[choice], reverse=reverse)


# 随机抽取index,给定列表长度，通过partsize来抽取下表，分为训练集与测试集
def chooseIndex(rangesize, partsize=8):
    trainindex = []
    testindex = []
    for i in range(rangesize):
        if (random.randint(1, partsize) != 3):
            trainindex.append(i)
        else:
            testindex.append(i)
    return trainindex, testindex


# 把list转换为partion连接的文本
def list2String(templist, partion=","):
    content = ''
    for i in range(len(templist)):
        content += (str(templist[i]) + partion)
    content=content[0:len(content)-1]
    return content


def md5Encode(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    return m2.hexdigest()

def Gzip(content):
    return gzip.compress(content)

def UnGzip(content):
    return gzip.decompress(content)
