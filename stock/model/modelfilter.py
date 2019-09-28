import numpy as np
import pandas as pd

labelRise = 5


# 30日线必须是上升得

def riseFilter(datafm, gap=-1, step=5):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60', 'volume', 'p_change']]
    datafm = np.array(datafm)
    close = datafm[:, 0]
    avg20 = datafm[:, 3]
    avg30 = datafm[:, 4]
    avg60 = datafm[:, 5]

    if (gap >= -step):
        label = (max(close[gap:]) / close[gap - 1] - 1) * 100
    else:
        label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100

    if label >= labelRise:
        label = 1
    else:
        label = 0

    max1 = max(close[gap - 8:gap])
    min1 = min(close[gap - 8:gap])
    increaseRatio = max1 / min1
    # 涨幅过高得不要
    if (increaseRatio > 2):
        return 0, label

    isSlowRise = 0
    isSlowRise1 = 0
    isSlowRise2 = 0
    if (np.mean(avg60[gap - 3:gap]) >= np.mean(avg60[gap - 6:gap - 3])
            and np.mean(avg60[gap - 9:gap - 6]) <= np.mean(avg60[gap - 6:gap - 3])):
        isSlowRise = 1
    if (np.mean(avg30[gap - 3:gap]) >= np.mean(avg30[gap - 6:gap - 3])
            and np.mean(avg30[gap - 9:gap - 6]) <= np.mean(avg30[gap - 6:gap - 3])):
        isSlowRise1 = 5
    if (np.mean(avg20[gap - 3:gap]) >= np.mean(avg20[gap - 6:gap - 3])
            and np.mean(avg20[gap - 9:gap - 6]) <= np.mean(avg20[gap - 6:gap - 3])):
        isSlowRise2 = 15

    flag = isSlowRise + isSlowRise1 + isSlowRise2
    if (flag > 20):
        flag = 1
    else:
        flag = 0
    return flag, label


# 历史有效上升得比例需要大于设定的ratio
def haveLabel(datafm, gap=-1, step=3, ratio=0.1, nolabel=False):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60', 'volume', 'p_change']]
    datafm = np.array(datafm)
    close = datafm[:, 0]

    labelorignal = 0
    label = 0
    if (nolabel == False):
        if (gap >= -step):
            label = (max(close[gap:]) / close[gap - 1] - 1) * 100
        else:
            label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100
        labelorignal = label
        if label >= labelRise:
            label = 1
        else:
            label = 0

    if (nolabel == False):
        pchange = datafm[-100 + gap:gap, 7]  #
    else:
        pchange = datafm[-100:gap, 7]  #
    pchange = [x for x in pchange if x > 5]

    if (len(pchange) > 100 * ratio):
        flag = 1
    else:
        flag = 0
    return flag, label, labelorignal


# 求每个区间的波动范围  standAndRise 需要细化  效果差
def standAndRise(datafm, gap=-1, step=3, nolabel=False):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60', 'volume', 'p_change']]
    datafm = np.array(datafm)
    close = datafm[:, 0]
    avg20 = datafm[:, 3]

    labelorignal = 0
    label = 0
    if (nolabel == False):
        if (gap >= -step):
            label = (max(close[gap:]) / close[gap - 1] - 1) * 100
        else:
            label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100
        labelorignal = label
        if label >= labelRise:
            label = 1
        else:
            label = 0

    bottomList = []
    topList = []
    # 求前五个区间的情况，每个区间间隔5，最大最小值
    for i in range(3):  # 测试了系数2，3,4，5，最终3较好
        if (nolabel == False):
            tempdata = avg20[gap - (i + 1) * 3:gap - i * 3]
        else:
            tempdata = avg20[-(i + 1) * 3:- i * 3]
        bottomList.append(min(tempdata))
        topList.append(max(tempdata))

    if (bottomList[2] >= bottomList[1] and bottomList[1] >= bottomList[0]):
        flag = 1
    else:
        flag = 0

    return flag, label, labelorignal


# 全部在线上  效果好 单独使用优于 haveLabel
def allStandAbove(datafm, gap=-1, step=3, nolabel=False):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60', 'volume', 'p_change']]
    datafm = np.array(datafm)
    close = datafm[:, 0]
    avg5 = datafm[:, 1]
    avg10 = datafm[:, 2]
    avg20 = datafm[:, 3]
    avg30 = datafm[:, 4]
    avg60 = datafm[:, 5]
    pchange = datafm[:, 7]

    labelorignal = 0
    label = 0
    if (nolabel == False):
        if (gap >= -step):
            label = (max(close[gap:]) / close[gap - 1] - 1) * 100
        else:
            label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100
        labelorignal = label
        if label >= labelRise:
            label = 1
        else:
            label = 0
    if (pchange[gap - 1] > 0 and pchange[gap - 2] > 0 and pchange[gap - 3] > 0 and pchange[gap - 4] > 0):
        flag = 0
        return flag, label, labelorignal

    if (nolabel == False and close[gap - 1] >= avg5[gap - 1]
            and close[gap - 1] >= avg10[gap - 1] and close[gap - 1] >= avg20[gap - 1]
            and close[gap - 2] >= avg5[gap - 2]
            and close[gap - 2] >= avg10[gap - 2] and close[gap - 2] >= avg20[gap - 2]):
        flag = 1
    elif (nolabel == True and close[- 1] >= avg5[- 1] and close[- 1] >= avg10[- 1] and close[- 1] >= avg20[- 1]):
        flag = 1
    else:
        flag = 0
    riseratio = [x for x in pchange[gap - 6:gap] if x > 0]
    rise1 = np.mean(avg60[gap - 3:gap]) - np.mean(avg60[gap - 6:gap - 3])
    rise2 = np.mean(avg30[gap - 3:gap]) - np.mean(avg30[gap - 6:gap - 3])
    rise3 = np.mean(avg20[gap - 3:gap]) - np.mean(avg20[gap - 6:gap - 3])

    if (flag == 1 and close[gap - 1] >= close[gap - 2] and pchange[gap - 1] >= 0
            and (rise1 >= 0 or rise2 >= 0 or rise3 >= 0) and len(riseratio) > 3):
        flag = 1
    else:
        flag = 0

    return flag, label, labelorignal


def slowRiseStand(datafm, gap=-1, step=4, nolabel=False):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30', 'oavg60', 'volume', 'p_change']]
    columnx = [x for x in datafm]
    if (gap + step < len(np.array(datafm))):
        ordata = np.array(datafm)[:gap + step, :]
    else:
        ordata = np.array(datafm)
    ordata = pd.DataFrame(ordata, columns=columnx)
    datafm = np.array(datafm)
    if (len(datafm) == 0):
        return -1, -1, -1, []
    close = datafm[:, 0]
    avg5 = datafm[:, 1]
    avg10 = datafm[:, 2]
    avg20 = datafm[:, 3]
    avg30 = datafm[:, 4]
    avg60 = datafm[:, 5]

    labelorignal = 0
    label = 0
    if (nolabel == False):
        if (gap >= -step):
            label = (max(close[gap:]) / close[gap - 1] - 1) * 100
        else:
            label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100
        labelorignal = label
        if label >= labelRise:
            label = 1
        else:
            label = 0

    max2 = max(close[gap - 10:gap])
    min2 = min(close[gap - 10:gap])
    increaseRatio = max2 / min2
    # 涨幅过高得不要
    if (increaseRatio > 1.2):
        return 0, label, labelorignal, ordata

    max3 = max(close[gap - 5:gap])
    min3 = min(close[gap - 5:gap])
    increaseRatio = max3 / min3
    # 涨幅过高得不要
    if (increaseRatio > 1.15):
        return 0, label, labelorignal, ordata

    if (avg5[gap - 1] / avg60[gap - 1] > 1.2 or avg60[gap - 1] / avg5[gap - 1] > 1.2):
        return 0, label, labelorignal, ordata

    isSlowRise2 = 0
    isSlowRise3 = 0
    if (np.mean(avg20[gap - 2:gap]) >= np.mean(avg20[gap - 4:gap - 2])):
        isSlowRise2 = 1

    if (avg5[gap - 1] >= avg5[gap - 3]):
        isSlowRise3 = 1
    flag = 0
    if (isSlowRise2 == 1 and isSlowRise3 == 1
            and (avg5[gap] > avg20[gap] or avg5[gap] > avg30[gap])
            and ((avg5[gap] - avg20[gap]) / avg20[gap] < 0.1
                 or (avg5[gap] - avg30[gap]) / avg30[gap] < 0.1)):
        if ((close[gap] - avg20[gap]) / avg20[gap] < 0.08
                or (close[gap] - avg30[gap]) / avg30[gap] < 0.08):
            flag = 1
    else:
        flag = 0

    if (flag == 1):  # 三天内存在粘合曲线，也就是有三条线是粘合度较高的
        flag = 0
        # 五日线上传 avg10,avg20
        if (avg5[gap - 1] > avg10[gap - 1] and avg5[gap - 1] > avg20[gap - 1]):
            flag = 1
        tempxx2 = np.mean(avg30[gap - 5:gap]) < np.mean(avg30[gap - 10:gap - 5])
        if (flag == 1 and tempxx2 > 0):
            flag = 1
        else:
            flag = 0

        tempxx3 = (max(avg30[gap - 2:gap]) - min(avg30[gap - 10:gap - 1])) / min(avg30[gap - 10:gap - 1])
        if (flag == 1 and tempxx3 < 0.06):
            flag = 1
        else:
            flag = 0

        if (flag == 1 and avg5[gap - 1] >= avg60[gap - 1]):
            flag = 1
        else:
            flag = 0

        rise1 = np.mean(avg60[gap - 5:gap]) - np.mean(avg60[gap - 10:gap - 5])
        rise2 = np.mean(avg60[gap - 10:gap - 5]) - np.mean(avg60[gap - 15:gap - 10])
        if (flag == 1 and rise1 > 0 and rise2 > 0 and avg5[gap - 1] > avg5[gap - 3]):
            flag = 1
        else:
            flag = 0

    return flag, label, labelorignal, ordata


# 下降三阴兵
def tiejinDrecress(close, avg, gap, pchange, open):
    if (close[gap - 2] <= avg[gap - 2] and close[gap - 1] <= avg[gap - 1]
            and close[gap - 1] <= avg[gap - 1] and open[gap - 2] < avg[gap - 2]):
        if (close[gap - 3] - avg[gap - 3] > -5 and close[gap - 2] - avg[gap - 2] > -5
                and close[gap - 1] - avg[gap - 1] > -5):
            if (pchange[gap - 2] + pchange[gap - 1] < -5):  # 可调
                return 1
            if (pchange[gap - 3] + pchange[gap - 2] + pchange[gap - 1] < -6):  # 可调
                if (pchange[gap - 1] < -2):
                    return 1
    return 0


# 顶部下降
def tiejinDrecressV2(close, avg, gap, pchange, open):
    if (close[gap - 4] >= avg[gap - 4] and close[gap - 3] >= avg[gap - 3]
            and close[gap - 2] <= avg[gap - 2]
            and close[gap - 1] <= avg[gap - 1]
            and open[gap - 1] < avg[gap - 1]):
        if (open[gap] < avg[gap] and pchange[gap - 1] < -2):  # 可调
            return 1
    return 0


# 不需要全部上涨得，这说明了运行到了中后期，反直觉
def tiejinDrecressV3(close, avg5, avg10, avg20, gap):
    if (avg5[gap - 1] > avg10[gap - 1] and avg10[gap - 1] > avg20[gap - 1] and
            avg5[gap - 2] > avg10[gap - 2] and avg10[gap - 2] > avg20[gap - 2] and
            avg5[gap - 3] > avg10[gap - 3] and avg10[gap - 3] > avg20[gap - 3]):
        rise = (close[gap - 1] - close[gap - 10]) / close[gap - 10]
        if (rise > 0):
            return 1
    return 0


# 三线下降
def openAnalysis(close, open, gap):
    if ((open[gap] - close[gap - 1]) / close[gap - 1] * 100 < -2.5):
        return 1
    return 0


# 挑选
def filter1(close, gap, avg10, avg20, avg5, pchange, open):

    if (tiejinDrecress(close, avg5, gap, pchange, open) == 1 or
            tiejinDrecress(close, avg10, gap, pchange, open) == 1):
        return -100

    if (tiejinDrecressV2(close, avg5, gap, pchange, open) == 1):
        return -100

    if (tiejinDrecressV3(close, avg5, avg10, avg20, gap) == 1):
        return -100

    if (openAnalysis(close, open, gap) == 1):
        return -100

    return 1



# 挑选
def filter1Info(close, gap, avg10, avg20, avg5, pchange, open):
    flags=[0,0,0,0]
    info=[]
    if (tiejinDrecress(close, avg5, gap, pchange, open) == 1 or
            tiejinDrecress(close, avg10, gap, pchange, open) == 1):
        flags[0]=-1
        info.append('下降三阴兵')

    if (tiejinDrecressV2(close, avg5, gap, pchange, open) == 1):
        flags[1] = -1
        info.append('顶部下降')

    if (tiejinDrecressV3(close, avg5, avg10, avg20, gap) == 1):
        flags[2] = -1
        info.append('全部上涨')

    if (openAnalysis(close, open, gap) == 1):
        flags[3] = -1
        info.append('三线下降')

    return flags,info

# 自定义退出
def getLabelMine(pchange, gap, step=3, top=12, min=-5):
    if (gap >= -step):
        return -100
    else:
        if (pchange[gap] < min):
            return min
        if (pchange[gap + 2] < -3):
            return pchange[gap] + pchange[gap + 1] - 3
        if (pchange[gap + 1] + pchange[gap] < 1):
            return 1

        if (pchange[gap + 1] < -5):
            return pchange[gap] - 5

        return pchange[gap] + pchange[gap + 1] + pchange[gap + 2]

    # 自定义退出


def getLabelMine2(pchange, gap, step=3):
    if (gap >= -step):
        return -100
    else:
        if (pchange[gap + 2] < -3):
            return pchange[gap] + pchange[gap + 1] - 3

        if (pchange[gap + 1] + pchange[gap] < 1):
            return max(pchange[gap + 1] + pchange[gap], -3)

        if (pchange[gap + 1] < -5):
            return pchange[gap] - 5

        return pchange[gap] + pchange[gap + 1] + pchange[gap + 2]


# 自定义退出
'''
较为复杂的逻辑
1.突破
2.调整 无效 ，第四天未突破前面的最高点
3.跌破 小于前四个的最低点

orignal: 5049 3.807 2.05 0.274
outlabel: 162 9.482 4.37 0.222
'''


def getLabelMine3(open, close, gap):
    if (gap > -3 or gap < 4 - len(open)):
        return -100
    else:
        temp = []
        temp.extend(open[gap - 5:gap - 1])
        temp.extend(close[gap - 5:gap - 1])
        topvalue = max(temp)
        if (close[gap - 1] < topvalue):  # 入场条件，突破，实际中还有支撑
            return -100

        breakpoint = close[gap - 1]
        begainpoint = -1
        for i in range(- gap):
            if (close[gap + i] > breakpoint):
                breakpoint = close[gap + i]  # 突破点
                begainpoint = i  # 更新
                if (gap + i == -1):
                    return max((close[-1] - close[gap - 1]) * 100 / close[gap - 1], -5)
                continue
            if (i - begainpoint <= 4):
                temp = []
                temp.extend(open[gap + begainpoint:gap + i])
                temp.extend(close[gap + begainpoint:gap + i])
                limitValue = min(temp)

                topvalue = max(close[gap + begainpoint:gap + i])
            else:
                temp = []
                temp.extend(open[gap + i - 4:gap + i])
                temp.extend(close[gap + i - 4:gap + i])
                limitValue = min(temp)
                topvalue = max(close[gap + i - 4:gap + i])

            if (close[gap + i] < limitValue):
                return max((close[gap + i] - close[gap - 1]) * 100 / close[gap - 1], -5)
            elif (i - begainpoint > 4 and close[gap + i] < topvalue):
                return max((close[gap + i] - close[gap - 1]) * 100 / close[gap - 1], -5)
            else:
                breakpoint = close[gap + i]  # 突破点
                begainpoint = i  # 更新

            if (gap + i == -1):
                return (close[-1] - close[gap - 1]) * 100 / close[gap - 1]

    return


# 理想最大退出结算
def getLabelBest(gap, close, step=3):
    if (gap >= -step):
        label = (max(close[gap:]) / close[gap - 1] - 1) * 100
    else:
        label = (max(close[gap:gap + step]) / close[gap - 1] - 1) * 100
    labelorignal = label
    return labelorignal


def getLabelBestNew(gap, close, step=3):
    if (gap >= -step):
        label = (close[-1] / close[gap - 1] - 1) * 100
    else:
        label = (close[gap + step] / close[gap - 1] - 1) * 100
    labelorignal = label
    return labelorignal


# 全部在线上  效果好 单独使用优于 haveLabel
def filterBad(datafm, gap=-1, step=3, nolabel=False):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30',
                     'oavg60', 'volume', 'p_change', 'high', 'low', 'open']]
    columnx = [x for x in datafm]
    if (gap + step < len(np.array(datafm))):
        ordata = np.array(datafm)[:gap + step, :]
    else:
        ordata = np.array(datafm)
    ordata = pd.DataFrame(ordata, columns=columnx)

    datafm = np.array(datafm)
    close = datafm[:, 0]
    avg5 = datafm[:, 1]
    avg10 = datafm[:, 2]
    avg20 = datafm[:, 3]
    avg30 = datafm[:, 4]
    avg60 = datafm[:, 5]
    volume = datafm[:, 6]
    pchange = datafm[:, 7]
    high = datafm[:, 8]
    low = datafm[:, 9]
    open = datafm[:, 10]

    labelbest = getLabelBestNew(gap, close)
    label1 = getLabelMine(pchange, gap)
    label2 = getLabelMine2(pchange, gap)
    label3 = getLabelMine3(open, close, gap)
    if (label1 == -100): return -100, [], []

    labels = [labelbest, label1, label2, label3]
    labels = [round(x, 3) for x in labels]
    return filter1(close, gap, avg10, avg20, avg5, pchange, open), labels, ordata,





# 全部在线上  效果好 单独使用优于 haveLabel
def filterBad2(datafm,gap=0):
    datafm = datafm[['close', 'oavg5', 'oavg10', 'oavg20', 'oavg30',
                     'oavg60', 'volume', 'p_change', 'high', 'low', 'open']]

    datafm = np.array(datafm)
    close = datafm[:, 0]
    avg5 = datafm[:, 1]
    avg10 = datafm[:, 2]
    avg20 = datafm[:, 3]
    avg30 = datafm[:, 4]
    avg60 = datafm[:, 5]
    volume = datafm[:, 6]
    pchange = datafm[:, 7]
    high = datafm[:, 8]
    low = datafm[:, 9]
    open = datafm[:, 10]

    return filter1Info(close, gap, avg10, avg20, avg5, pchange, open)
