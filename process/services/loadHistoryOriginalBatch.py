import process.loadInfo.getTsHistoryStockFile as history
from multiprocessing.dummy import Pool as ThreadPool
import www.stList as consts

SuccessList = []

# 按照行读取
def getStockSet(fileName):  # general function to parse tab -delimited floats
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        temp = line.replace("\n", "")
        dataMat.append(temp)
    return dataMat

import www.config_default as config

def getinfo(stockname,His=False,type=config.period):
    # 时间 开盘 收盘  最高 最低 成交量
    startTime = '2012-02-01'
    if(His==False):
        startTime='2016-04-01'
    try:
        if(His==True):
            history.getHistoryFile(stockname,type,startTime)
        else:
            history.getHistoryFile(stockname, type, startTime, True)
    except:
        1


def getstockinfoList(stocklist):
    pool2 = ThreadPool(16)
    pool2.map(getinfo, stocklist)
    return 0;



def process():
    listtrain= consts.needStockM
    getstockinfoList(listtrain)




