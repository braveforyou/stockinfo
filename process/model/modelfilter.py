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


# 5下交叉10 均在20以上，可等待买入
def tiejinDrecressV4(avg5, avg10, avg20, gap):
    if (avg5[gap - 1] < avg10[gap - 1] and avg10[gap - 1] > avg20[gap - 1] and
            avg5[gap - 2] < avg10[gap - 2] and avg10[gap - 2] > avg20[gap - 2] and
            avg5[gap - 3] < avg10[gap - 3] and avg10[gap - 3] > avg20[gap - 3]):
        # if(pchange[gap-1]>0):
        return 1

    return 0


# 挑选
def filter1Info(close, gap, avg10, avg20, avg5, pchange, open):
    flags = []

    # 5_10_20这个形态特别厉害 通道调整
    if (tiejinDrecressV4(avg5, avg10, avg20, gap) == 1):
        flags.append(1)
    else:
        flags.append(0)
    # 下降三阴兵
    if (tiejinDrecress(close, avg5, gap, pchange, open) == 1 or
            tiejinDrecress(close, avg10, gap, pchange, open) == 1):
        flags.append(-1)
    else:
        flags.append(0)

    # 顶部下降
    if (tiejinDrecressV2(close, avg5, gap, pchange, open) == 1):
        flags.append(-1)
    else:
        flags.append(0)

    # 纯加速上升通道
    if (tiejinDrecressV3(close, avg5, avg10, avg20, gap) == 1):
        flags.append(-1)
    else:
        flags.append(0)
    # 三线下降
    if (openAnalysis(close, open, gap) == 1):
        flags.append(-1)
    else:
        flags.append(0)

    return flags


# 挑选最近回落或者横盘的來算
def huiluoHenPan(close, gap, avg10, avg20, avg5, pchange, open):
    flags = [-1]
    temp = close[-6:]
    max = np.max(temp)
    min = np.min(temp)

    # 窄幅震荡
    if ((max - min) / min < 0.08):
        flags[0] = 1
    # 在下跌，选择在调整状态的
    if ((close[-1] - close[-5]) / close[-5] > -0.25 and (close[-1] - close[-5]) / close[-5] < -0.05):
        flags[0] = 1

    return flags


# 5下交叉10 均在20以上，且量下降，可等待买入
def decressAdjust(avg5, avg10, avg20, close, volume, avg30):
    gap = -1
    volumeNear = np.mean(volume[gap - 10:gap])
    volumeFar = np.mean(volume[gap - 14:gap - 4])

    avg30riseNear = np.mean(avg30[gap - 10:gap])
    avg30riseFar = np.mean(avg30[gap - 14:gap - 4])

    avg20riseNear = np.mean(avg20[gap - 10:gap])
    avg20riseFar = np.mean(avg20[gap - 14:gap - 4])

    above520 = False

    if (avg5[gap] > avg20[gap] and avg5[gap - 1] > avg20[gap - 1] and avg5[gap - 2] > avg20[gap - 2]):
        above520 = True

    if ((avg5[gap] - avg5[gap - 5]) / avg5[gap - 5] <= 0.05): return 0  # 在爬升

    avg5Decress = True if np.mean(avg5[gap - 5:gap]) < np.mean(avg5[gap - 8:gap - 2]) else False  # 曲线上升为好

    decress = True if (volumeNear < volumeFar) else False
    if (decress == True and avg5[gap] > avg5[gap - 1] and above520 == True and avg5Decress == False
            and (avg10[gap] > avg20[gap])
            and (avg30riseFar < avg30riseNear or avg20riseNear > avg20riseFar)):
        return 1
    if (decress == True and close[gap] > avg5[gap] and above520 == True and avg5Decress == False
            and (avg10[gap] > avg20[gap])
            and (avg30riseFar < avg30riseNear or avg20riseNear > avg20riseFar)):
        return 1
    return -1


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


# line1 交叉line2 得近似方法
def isjiaocha(line1, line2):
    lineLen = len(line1)
    existlow = [1 for i in range(int(lineLen / 2)) if line1[i] < line2[i]]
    existRise = [1 for i in range(lineLen) if i >= lineLen / 2 and line1[i] > line2[i]]
    if (len(existlow) > 0 and len(existRise) > 0):
        return 1
    return 0


# 近五日内发生多次交叉，或者上扬
def jiaochaBegain(avg5, avg10, avg20, avg30, gap, range=6):
    if (gap - range + len(avg5) < 0): return -1

    avg5 = avg5[gap - range:gap]
    avg10 = avg10[gap - range:gap]
    avg20 = avg20[gap - range:gap]
    avg30 = avg30[gap - range:gap]

    jiaocha510 = isjiaocha(avg5, avg10)
    jiaocha520 = isjiaocha(avg5, avg20)
    jiaocha530 = isjiaocha(avg5, avg30)
    jiaocha1020 = isjiaocha(avg10, avg20)
    jiaocha1030 = isjiaocha(avg10, avg30)
    jiaocha2030 = isjiaocha(avg20, avg30)

    riseLimit = True if (avg5[-1] - avg5[- range]) / avg5[- range] < 0.08 and (avg5[-1] - avg5[- 3]) / avg5[
        - 3] > 0.02 else False

    if (riseLimit and jiaocha510 + jiaocha530 + jiaocha520 + jiaocha1020 + jiaocha1030 + jiaocha2030 >= 3):
        return 1

    return 0

import www.config_default as config

# 近五日内发生多次交叉，或者上扬
def reachKeyLine(close, avg30, avg60):
    ratio1 = (close[-1] - avg30[-1]) / close[-1]
    ratio2 = (close[-1] - avg60[-1]) / close[-1]

    mean30_close = np.mean(avg30[-3:])
    mean30_far = np.mean(avg30[-6:-3])

    mean60_close = np.mean(avg60[-3:])
    mean60_far = np.mean(avg60[-6: -3])

    raiseRatio = (close[-1] - close[-3]) / close[-3]



    if (raiseRatio >= 0.03): return 0

    thread=0.05
    if(config.period=='W'):
        thread=0.08

    if (((ratio1 <=thread and ratio1 >= -0.01) or (ratio2 <= thread and ratio2 >= -0.01))
            and (mean30_close >= mean30_far or mean60_close >= mean60_far)):
        return 2

    return 0


# 全部在线上  效果好 单独使用优于 haveLabel
def filterBad2(datafm, gap=0):
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

    result = []
    try:
        flag = decressAdjust(avg5, avg10, avg20, close, volume, avg30)
        result.append(flag)
    except:
        1
    try:
        flag = jiaochaBegain(avg5, avg10, avg20, avg30, gap, 5)
        result.append(flag)
    except:
        1
    try:
        flag = jiaochaBegain(avg5, avg10, avg20, avg30, gap, 4)
        result.append(flag)
    except:
        1
    try:
        flag = jiaochaBegain(avg5, avg10, avg20, avg30, gap, 3)
        result.append(flag)
    except:
        1

    try:
        flag = reachKeyLine(close, avg30, avg60)
        result.append(flag)
        if (flag == 2):
            return [2]
    except:
        raise
        1

    if (sum(result) >= 1):
        return [1]
    return [0]
