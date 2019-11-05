'''
实验模型

'''
import process.model.modelfilter as filter
import time
import warnings
import pandas as pd
import process.services.expendFeaturesBatchHis as expendFeature
import www.config_default as config

warnings.filterwarnings('ignore')
start = time.time()


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
        if (config.debug==False):
            dataframe = expendFeature.process(item)
        else:
            filename = "D:\PythonTrain\\stockListExpend\\" + str(item) + ".csv"
            dataframe = pd.read_csv(filename)

        flag = filter.filterBad2(dataframe)

        if (sum(flag) > -1):
            lock.acquire()  # 加锁
            needList.append(['st' + str(item), str(flag)])
            lock.release()
    except FileNotFoundError:
        1
    except :
        raise
