import process.loadInfo.base.getTsHistoryStockFile as history
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


def getinfo(stockname,His=False):
    # 时间 开盘 收盘  最高 最低 成交量
    startTime = '2016-02-01'
    if(His==False):
        startTime='2019-04-01'
        print(His)
    try:
        if(His==True):
            history.getHistoryFile(stockname,'D',startTime)
        else:
            history.getHistoryFile(stockname, 'D', startTime, True)
    except:
        1


def getstockinfoList(stocklist):
    pool2 = ThreadPool(16)
    pool2.map(getinfo, stocklist)
    return 0;


def process():
    listtrain= consts.needStockM
    getstockinfoList(listtrain)
