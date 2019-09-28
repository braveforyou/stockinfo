import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from stock import baseinfo as ovserve, baseinfo as seaplt

'''
筛选出表现较好的
1.先设计能描述其性能得指标，以及滑动窗口

先用逻辑回归来做，600个点  400个点 200个点

'''


def getfeatures(filename):
    data = pd.read_csv(filename)[['date', 'close', 'p_change']]
    data = np.array(data)
    for i in range(len(data)):
        data[i][0] = i

    return data


# 获取权重，看出其斜率，X是1到600，Y是价格
def getWeight(data, show=False, filename=""):
    lgr = LinearRegression()
    lgr.fit(data[:, 0].reshape(len(data), 1), data[:, 1])
    divide = ((lgr.predict(data[:, 0].reshape(len(data), 1)) - data[:, 1]) / data[:, 1]) ** 2

    if (show == True):
        seaplt.plotTwoDimenSionWithLine(data[:, 0], data[:, 1], lgr.predict(data[:, 0].reshape(len(data), 1)),
                                        filename=filename)

    return lgr.coef_, np.mean(divide)


def analysis(data):
    # 6月线  一个月20个交易日   3月线
    data0 = data[-30:]  # 短期内趋势
    data1 = data[-60:]  # 3月内趋势
    data2 = data[-120:]  # 6月内趋势
    data3 = data[-240:]  # 1年内趋势

    max1 = max(data1[:, 1])
    min1 = min(data1[:, 1])
    current = np.mean(data1[:, 1])
    # 3个月内最大涨幅
    increaseRatio = max1 / min1

    weight0, divide0 = getWeight(data0)
    weight1, divide1 = getWeight(data1)
    weight2, divide2 = getWeight(data2)
    weight3, divide3 = getWeight(data3)


    weightList = []
    weightList.append(weight1[0])
    weightList.append(weight2[0])
    weightList.append(weight3[0])
    weightList.append(weight0[0])

    return weightList, increaseRatio, data0, current


def filterByWeight(dirname="D:\\PythonTrain\\stockList"):
    fileList = FileUtil.getDirFileName(dirname)
    result = []
    for item in fileList:
        data = getfeatures(item)
        weightList, increaseRatio, datar, current = analysis(data)
        if (current < 1 or current > 50): continue
        stockname = item.split("\\")[-1].split(".")[0]
        # 筛掉各个时间维度都在下降得
        if (weightList[1] < 0 and weightList[2] < 0 and weightList[3] < 0):  # j近半年
            continue
        else:
            # 查找近期得趋势维度
            if (weightList[0] >= 0 or weightList[1] >= 0 or weightList[2] >= 0):
                result.append(stockname)

    return result


def filterIncrease(dirname="D:\\PythonTrain\\stockList", needStock=[]):
    fileList = FileUtil.getDirFileName(dirname)
    result = []
    filterTarget = []
    # 3月 6月 1年 600交易日
    filterStock = []
    for item in fileList:
        print(item)
        try:
            stockname = item.split("\\")[-1].split(".")[0]
            if (str(stockname) not in needStock): continue
            data = getfeatures(item)
            weightList, increaseRatio, data4, min1 = analysis(data)

            # 筛掉各个时间维度都在下降得
            print(increaseRatio)
            if (increaseRatio >= 2):
                filterStock.append(stockname)
            else:
                filename = "D:\\PythonTrain\\stimg\\" + str(stockname) + ".jpg"
                print(filename)
                result.append(stockname)
                ovserve.observeSingleDistribution(filterTarget, filename)
                getWeight(data4, True, filename)
            filterTarget.append(increaseRatio)
        except:
            1

    return result, filterStock


needStock = filterByWeight("D:\\PythonTrain\\stockList")

needStock2, filterStock2 = filterIncrease("D:\\PythonTrain\\stockList", needStock)
print(len(needStock2))
print(needStock2)
