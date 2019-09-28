import pandas as pd
import numpy as np



'''
1.DIF、DEA均为正，DIF向上突破DEA，买入信号参考。

2.DIF、DEA均为负，DIF向下跌破DEA，卖出信号参考。

3.DIF线与K线发生背离，行情可能出现反转信号。

4.DIF、DEA的值从正数变成负数，或者从负数变成正数并不是交易信号，因为它们落后于市场。
'''

def smaCal(tsPrice, k):
    Sma = pd.Series(0.0, index=tsPrice.index)
    for i in range(k - 1, len(tsPrice)):
        Sma[i] = sum(tsPrice[(i - k + 1):(i + 1)]) / k
    return (Sma)


def wmaCal(tsPrice, weight):
    k = len(weight)
    arrWeight = np.array(weight)
    Wma = pd.Series(0.0, index=tsPrice.index)
    for i in range(k - 1, len(tsPrice.index)):
        Wma[i] = sum(arrWeight * tsPrice[(i - k + 1):(i + 1)])
    return (Wma)


def ewmaCal(tsprice, period=5, exponential=0.2):
    Ewma = pd.Series(0.0, index=tsprice.index)
    Ewma[period - 1] = np.mean(tsprice[0:period])
    for i in range(period, len(tsprice)):
        Ewma[i] = exponential * tsprice[i] + (1 - exponential) * Ewma[i - 1]

    return (Ewma)


def getthored(x):
    if (x > 0):
        x = 1
    else:
        x = -1
    return x


def getdecision(dif, dea):
    decision = []
    for i in range(len(dif)):
        if (dea[i] > 0 and dif[i] > dea[i]):
            decision.append(1)
        elif (dea[i] < 0 and dif[i] < 0 and dif[i] < dea[i]):
            decision.append(-1)
        else:
            decision.append(0)
    return decision

    # DIF = EMA12 – EMA26
def getmacd(closeData, fast=12, slow=26, nsig=5, choice=1):
    if (choice != 1):

        dif = ewmaCal(closeData, fast, 2 / (1 + fast)) / ewmaCal(closeData, slow, 2 / (1 + slow)) * 100 - 100
    else:
        dif = ewmaCal(closeData, fast, 2 / (1 + fast)) - ewmaCal(closeData, slow, 2 / (1 + slow))

    dea = ewmaCal(dif, nsig, 2 / (1 + nsig))
    macd = dif - dea
    dif2 = [getthored(x) for x in dif]
    dea2 = [getthored(x) for x in dea]

    diftrend = []
    for i in range(len(dif)):
        if (i == 0):
            diftrend.append(dif[0])
        else:
            diftrend.append(dif[i] - dif[i - 1])
    deatrend = []
    for i in range(len(dea)):
        if (i == 0):
            deatrend.append(dea[0])
        else:
            deatrend.append(dea[i] - dea[i - 1])

    difdeamix = [x * dea2[i] for i, x in enumerate(dif)]
    decision = getdecision(dif, dea)
    return macd, dif, dea, dif2, dea2, difdeamix, diftrend, deatrend, decision
