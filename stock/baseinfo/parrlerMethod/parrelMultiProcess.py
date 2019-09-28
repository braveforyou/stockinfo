
'''
实验模型

'''
import stock.model.modelfilter as filter
from stock.pltInfo.pltAvgLines import *
import warnings
warnings.filterwarnings('ignore')
import time
import multiprocessing
start = time.time()

from multiprocessing import Lock,Manager


def analysis(allLabels):
    try:
        allLabels=[float(x) for x in allLabels if x!=-100]
        print('count:',len(allLabels),'mean:', round(np.mean(allLabels), 3),'median:', round(np.median(allLabels), 3),
          'errorRatio:',round(len([x for x in allLabels if x <= 0]) / len(allLabels), 3))
    except:
        print('---------------')

#内部单个执行逻辑
def inner(item):
    datasize = 80
    step = 4
    filename = "D:\PythonTrain\\stockListExpend\\" + str(item) + ".csv"
    dataframe = pd.read_csv(filename)

    try:
        for i in range(3, datasize, step):
            flag, labels, datafm = filter.filterBad(dataframe, -i, step)
            if (len(labels) == 0): continue
            if (flag != -100):
                lock.acquire()  # 加锁
                needList.append(labels)
                lock.release()
            else:
                filterContent.append(labels)
    except:
        raise
        1
    return 1

#初始化加锁机共享变量
def init(l,l2,l3):
    global lock
    global needList
    global filterContent
    lock = l
    needList=l2
    filterContent=l3

if __name__ == '__main__':
    manager = Manager()
    cpu_count = multiprocessing.cpu_count()
    print('Cpu count:', cpu_count)
    lock = Lock()
    needList=manager.list()
    filterContent=manager.list()
    #初始化进程池
    pool = multiprocessing.Pool(cpu_count,initializer=init, initargs=(lock,needList,filterContent,))
    pool.map(inner,  consts.needStockM)


    needList=np.array(needList)
    filterContent=np.array(filterContent)
    for i in range(len(needList[0])):
        analysis(list(needList[:, i]))

    end = time.time()
    print('Cost time:', end - start)