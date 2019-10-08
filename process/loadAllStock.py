'''
实验模型

'''
import process.model.modelfilter as filter
import time
import warnings
import pandas as pd
import numpy as np
import process.expendFeaturesBatchHis as expendFeature

warnings.filterwarnings('ignore')
start = time.time()


def analysis(allLabels):
    try:
        allLabels = [float(x) for x in allLabels if x != -100]
        print('count:', len(allLabels), 'mean:', round(np.mean(allLabels), 3), 'median:',
              round(np.median(allLabels), 3),
              'errorRatio:', round(len([x for x in allLabels if x <= 0]) / len(allLabels), 3))
    except:
        1


def initStParam(l, l2, l3, l4, l5):
    global lock
    global needList
    global filterContent
    global needAvg
    global filterAvg
    lock = l
    needList = l2
    filterContent = l3
    needAvg = l4
    filterAvg = l5


def inner(item):
    try:
        # dataframe = expendFeature.process(item)
        filename = "D:\PythonTrain\\stockListExpend\\" + str(item) + ".csv"
        dataframe = pd.read_csv(filename)

        flag = filter.filterBad2(dataframe)

        if (sum(flag) > -1 ):
            lock.acquire()  # 加锁
            needList.append(['st' + str(item), str(flag)])
            lock.release()
    except:
        1
