import process.loadInfo.base.company as company
import pandas as pd
import numpy as np



def initStParam(l, l2, l3,l4):
    global lock
    global listFilter
    global listNeed
    global contents
    lock = l
    listFilter = l2
    listNeed = l3
    contents=l4



def analysisInner(stname):
    stname=stname[1]
    tempdict = {}
    tempdict['name'] = str(stname)

    每股中报收益详情, 每股一季度报收益详情, 中报每股收益下降, 中报收益各年, 增速提高 = company.getCompanyInfo(stname)

    tempdict['companyInfo_middleMeiGuReport'] = 每股中报收益详情
    tempdict['companyInfo_oneQuartMeiGuReport'] = 每股一季度报收益详情

    baseinfo = company.getBaseInfo(stname)
    stnamex = str(baseinfo[0])
    if (len(stnamex) != 6):
        for i in range(6 - len(stnamex)):
            stnamex = '0' + stnamex
        stnamex = 'sz' + stnamex
    else:
        stnamex = 'sh' + stnamex

    baseinfo[0] = stnamex

    tabelShow = []
    tabelShow.append(中报每股收益下降)  # 每股收益下降w
    tabelShow = [float(x) for x in tabelShow]
    tabelShow.append(增速提高)  # 每股收益下降w
    # if(中报收益各年[0]<0 and 中报收益各年[0]!=-100):continue#进一季度的每股收益率

    sallaryPerSt = baseinfo[-1]  # 每股价格
    stname = stname.replace('st', '')
    priceNow = pd.read_csv("D:\PythonTrain\stockListNow\\" + stname + ".csv")
    priceLatest = np.array(priceNow)[0, 3]
    priceMax = np.max(np.array(priceNow)[:, 3])
    priceNow = np.array(priceNow)[-1, 3]

    expectSallary100 = sallaryPerSt * 100 / priceNow
    gonggao = company.getCompanyGonGao(stname)

    jiejing = 0
    xianshou = -1
    zengchi = 0
    if (len(gonggao) > 0):
        for i in range(len(gonggao)):
            if (gonggao[i][1].find('解禁')):
                jiejing = -1
            if (gonggao[i][1].find('限售')):
                xianshou = -1
            if (gonggao[i][1].find('增持')):
                zengchi = 1
    tabelShow.append(jiejing)  # 解禁
    tabelShow.append(xianshou)  # 限售
    tabelShow.append(zengchi)

    tempdict['refuseInfo'] = tabelShow
    tempdict['score'] = sum(tabelShow)
    tempdict['baseinfo'] = baseinfo
    tempdict['expectSallary100'] = round(expectSallary100)
    tempdict['reportInfo'] = gonggao

    tempdict['currentrise'] = round((priceNow - priceLatest) / priceLatest * 100, 2)
    tempdict['maxrise'] = round((priceMax - priceLatest) / priceLatest * 100, 2)
    tempdict['currentPrice'] = round(priceNow, 2)

    needflag = True
    if (中报收益各年[0] < 0 and 中报收益各年[0] != -100 or tempdict['currentrise'] < 10):
        listNeed.append(stname)
        contents.append(tempdict)
    else:
        needflag=False
        listFilter.append(stname)
    return tempdict, needflag
