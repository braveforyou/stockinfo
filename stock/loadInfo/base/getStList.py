import tushare as ts
import numpy as np

#获取所有代码
def getStList():
    stlist = ts.get_industry_classified()
    stlist = np.array(stlist)
    return stlist[:, 0]
