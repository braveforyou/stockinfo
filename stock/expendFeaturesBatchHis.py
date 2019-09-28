
from stock.model.base.MACD import *

def getData(stname,His=False):
    column = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change', 'ma5', 'ma10', 'ma20',
              'v_ma5', 'v_ma10', 'v_ma20']

    if(His==False):
        data = pd.read_csv("D:\\PythonTrain\\stockListNow\\" + stname + ".csv")[column]
    else:
        data = pd.read_csv("D:\\PythonTrain\\stockList\\" + stname + ".csv")[column]
    closeData = data['close']
    data = np.array(data)
    return data, closeData


# 当前值与前N日的均值的比值1.x
def anlysisiColumnAvg(data, windowsSize,datasize=200):
    datatemp = pd.Series(data).rolling(window=windowsSize).mean()
    data = data / datatemp - 1
    return np.array(data[-datasize:]), np.array(datatemp[-datasize:])


def anlysisiColumnSum(data, closeData, windowsSize,datasize=200):
    datatemp = pd.Series(data).rolling(window=windowsSize).sum()

    data = datatemp / closeData
    return np.array(data[-datasize:])


def anlysisiColumnLabel(data, windowsSize, raiseRatio=0.06,datasize=200):
    label = []
    rise = []
    down = []
    for i in range(len(data)):
        # 边界，最近的几条数据
        if (len(data[i + 1:i + windowsSize + 1]) < windowsSize):
            label.append(-1)
            rise.append(-1)
            down.append(-1)
        else:
            temp = max(data[i + 1:i + windowsSize + 1]) / data[i] - 1
            down.append(min(data[i + 1:i + windowsSize + 1]) / data[i] - 1)
            if (temp > raiseRatio):
                label.append(1)
            else:
                label.append(0)
            rise.append(temp)

    return np.array(label[-datasize:]), np.array(rise[-datasize:]), np.array(down[-datasize:])


# 获取均线信息
def getPriceAvgLine(data,datasize):
    avgList5, avg5 = anlysisiColumnAvg(data, 5,datasize)
    avgList10, avg10 = anlysisiColumnAvg(data, 10,datasize)
    avgList20, avg20 = anlysisiColumnAvg(data, 20,datasize)
    avgList30, avg30 = anlysisiColumnAvg(data, 30,datasize)
    avgList60, avg60 = anlysisiColumnAvg(data, 60,datasize)

    divide510 = avgList5 - avgList10
    divide520 = avgList5 - avgList10
    divide530 = avgList5 - avgList10
    divide560 = avgList5 - avgList10
    divide1020 = avgList10 - avgList20
    divide1030 = avgList10 - avgList30
    divide1060 = avgList10 - avgList60
    divide2030 = avgList20 - avgList30
    divide2060 = avgList20 - avgList60
    divide3060 = avgList30 - avgList60

    return avgList5, avgList10, avgList20, avgList30, avgList60, \
           divide510, divide520, divide530, divide560, divide1020, divide1030, \
           divide1060, divide2030, divide2060, divide3060, avg5, avg10, avg20, avg30, avg60


# 获取均线信息
def getVolumeAvgLine(data,datasize):
    avgList2, x1 = anlysisiColumnAvg(data, 2,datasize)
    avgList3, x2 = anlysisiColumnAvg(data, 3,datasize)
    avgList5, x3 = anlysisiColumnAvg(data, 5,datasize)
    avgList10, x4 = anlysisiColumnAvg(data, 10,datasize)
    return avgList2, avgList3, avgList5, avgList10


# 获取累计价格变化信息
def getRaise(data, closeData,datasize=200):
    raiseList3 = anlysisiColumnSum(data, closeData, 3,datasize)
    raiseList5 = anlysisiColumnSum(data, closeData, 5,datasize)
    raiseList10 = anlysisiColumnSum(data, closeData, 10,datasize)
    return raiseList3, raiseList5, raiseList10


# 获取累计价格变化信息
def getLabel(data,datasize=200):
    label3, rise, down = anlysisiColumnLabel(data, 3,datasize=datasize)
    return label3, rise, down




def process(stname,His=False):
    column = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change', 'ma5', 'ma10',
              'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'raise3', 'raise5', 'raise10',
              'avg5', 'avg10', 'avg20', 'avg30', 'avg60',
              'avg2v', 'avg3v', 'avg5v', 'avg10v',
              'divide510', 'divide520', 'divide530',
              'divide560', 'divide1020', 'divide1030', 'divide1060', 'divide2030',
              'divide2060', 'divide3060',
              'macd', 'dif', 'dea', 'dif2', 'dea2', 'difdeamix', 'diftrend', 'deatrend', 'decision',
              'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60',
              'label', 'orise', 'odown', 'stockname']
    result = []
    datasize=200
    if(His==False):
        datasize=30
    try:
        data, closeData = getData(stname,His)
        if (len(data) < datasize): return []
        macd, dif, dea, dif2, dea2, difdeamix, diftrend, deatrend, decision = getmacd(closeData, 10, 20, 5)
        macd = np.array(macd)[-datasize:]
        dif = np.array(dif)[-datasize:]
        dea = np.array(dea)[-datasize:]
        dif2 = np.array(dif2)[-datasize:]
        dea2 = np.array(dea2)[-datasize:]
        difdeamix = np.array(difdeamix)[-datasize:]
        diftrend = np.array(diftrend)[-datasize:]
        deatrend = np.array(deatrend)[-datasize:]
        decision = np.array(decision)[-datasize:]

        avgList5, avgList10, avgList20, avgList30, avgList60, divide510, divide520, divide530, \
        divide560, divide1020, divide1030, divide1060, divide2030, divide2060 \
            , divide3060, avg5, avg10, avg20, avg30, avg60 = getPriceAvgLine(data[:, 3],datasize)
        avgList2V, avgList3V, avgList5V, avgList10V = getVolumeAvgLine(data[:, 5],datasize)
        raiseList3, raiseList5, raiseList10 = getRaise(data[:, 6], data[:, 3],datasize)
        label3, rise, down = getLabel(data[:, 3],datasize)
        #print(len(label3),len(data),datasize)
        data = np.c_[data[-datasize:], raiseList3]
        data = np.c_[data[-datasize:], raiseList5]
        data = np.c_[data[-datasize:], raiseList10]

        data = np.c_[data[-datasize:], avgList5]
        data = np.c_[data[-datasize:], avgList10]
        data = np.c_[data[-datasize:], avgList20]
        data = np.c_[data[-datasize:], avgList30]
        data = np.c_[data[-datasize:], avgList60]

        data = np.c_[data[-datasize:], avgList2V]
        data = np.c_[data[-datasize:], avgList3V]
        data = np.c_[data[-datasize:], avgList5V]
        data = np.c_[data[-datasize:], avgList10V]

        data = np.c_[data[-datasize:], divide510]
        data = np.c_[data[-datasize:], divide520]
        data = np.c_[data[-datasize:], divide530]
        data = np.c_[data[-datasize:], divide560]

        data = np.c_[data[-datasize:], divide1020]
        data = np.c_[data[-datasize:], divide1030]
        data = np.c_[data[-datasize:], divide1060]
        data = np.c_[data[-datasize:], divide2030]
        data = np.c_[data[-datasize:], divide2060]
        data = np.c_[data[-datasize:], divide3060]

        data = np.c_[data[-datasize:], macd]
        data = np.c_[data[-datasize:], dif]
        data = np.c_[data[-datasize:], dea]
        data = np.c_[data[-datasize:], dif2]
        data = np.c_[data[-datasize:], dea2]
        data = np.c_[data[-datasize:], difdeamix]
        data = np.c_[data[-datasize:], diftrend]
        data = np.c_[data[-datasize:], deatrend]
        data = np.c_[data[-datasize:], decision]

        data = np.c_[data[-datasize:], avg5]
        data = np.c_[data[-datasize:], avg10]
        data = np.c_[data[-datasize:], avg20]
        data = np.c_[data[-datasize:], avg30]
        data = np.c_[data[-datasize:], avg60]
        data = np.c_[data[-datasize:], label3]
        data = np.c_[data[-datasize:], rise]
        data = np.c_[data[-datasize:], down]
        stockname = [stname for i in list(range(datasize))]
        data = np.c_[data[-datasize:], stockname]
        if (len(result) == 0):
            result = data
        else:
            result = np.vstack((result, data))
    except:
        1
    needcolumn = ['date','volume','high','low','open','p_change' ,'close', 'raise3', 'raise5', 'raise10',
                  'avg5', 'avg10', 'avg20', 'avg30', 'avg60',
                  'avg2v', 'avg3v', 'avg5v', 'avg10v',
                  'divide510', 'divide520', 'divide530',
                  'divide560', 'divide1020', 'divide1030', 'divide1060', 'divide2030',
                  'divide2060', 'divide3060',
                  'macd', 'dif', 'dea', 'dif2', 'dea2', 'difdeamix', 'diftrend', 'deatrend', 'decision',
                  'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60',
                  'label', 'orise', 'odown', 'stockname']
    filename="D:\PythonTrain\\stockListExpend\\"+str(stname)+".csv"
    if(len(result)<10):return
    pd.DataFrame(result, columns=column)[needcolumn].to_csv(filename)
    return pd.DataFrame(result, columns=column)[needcolumn]
