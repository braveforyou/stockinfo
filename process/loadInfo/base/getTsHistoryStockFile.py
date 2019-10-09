import tushare as ts
import datetime
import pandas as pd
import numpy as np
# 获取时间段内的历史记录
'''
    date：日期
    open：开盘价
    high：最高价
    close：收盘价
    low：最低价
    volume：成交量
    price_change：价格变动
    p_change：涨跌幅
    ma5：5日均价
    ma10：10日均价
    ma20:20日均价
    v_ma5:5日均量
    v_ma10:10日均量
    v_ma20:20日均量
    turnover:换手率[注：指数无此项]
'''
column = ['date', 'open', 'high', 'close', 'low', 'volumn', ' p_chang', 'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10',
          'v_ma20']




# 获取得数据不完整
def getHistoryFile(code, type='D', startTime='2016-01-01',current=False):
    now_time = datetime.datetime.now()
    data = ts.get_hist_data(code, start=startTime, end=now_time.strftime('%Y-%m-%d'), ktype=type)
    closeData = np.array(data['close'])
    if (closeData[0] > 50 or closeData[0] < 1):
        return

    if (current == False):
        filename = "D:\PythonTrain\stockList\\" + str(code) + ".csv"
    else:
        filename = "D:\PythonTrain\stockListNow\\" + str(code) + ".csv"
    data = data.sort_values(by="date", ascending=True)

    if(len(np.array(closeData))<60):return

    data.to_csv(filename)
    return
