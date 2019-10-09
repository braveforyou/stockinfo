
import tushare as ts
import numpy as np


needStockM  = ['300193', '300003', '002274', '601155', '600585', '000672', '300609', '000596', '300378', '601939',
              '300586', '600829', '603568', '603860', '000799', '000582', '000002', '002368',
              '002262', '603360', '601668', '600206', '600589', '300450', '000661', '002125',
              '000029', '603181', '002301', '300546', '300339', '600085', '603167', '002371', '002372', '600667',
              '300635', '000860', '300639', '000858', '600118', '002916', '002414', '300725', '002463', '000001',
              '002402', '300735', '603679', '300667', '300132', '002304', '002853', '600809', '002939','600048',
              '002153', '600557', '600801', '603939', '600031', '300584', '600070', '300045', '300661',
              '600009', '000733', '300207', '300394', '600438', '603496', '603429', '000708', '300429', '002182',
              '300470', '300579', '603233', '000739', '603667', '600260', '600436', '300463', '600639', '002415',
              '002637', '603326', '002117', '600566', '000682', '300628', '600620', '002146', '002885',
              '300563', '600067', '002867', '002511', '600779', '601618', '300383', '002243', '002179', '603899',
              '300607', '002142', '603416', '600036', '603199', '300595', '603520', '002624', '600519', '603369',
              '600887', '002214', '600900', '600559', '000938', '603129', '600845', '601328', '300638', '600872',
              '002892', '002675', '601288', '603883', '600273']



#获取所有代码
def getStList():
    stlist = ts.get_industry_classified()
    stlist = np.array(stlist)
    return stlist[:, 0]
