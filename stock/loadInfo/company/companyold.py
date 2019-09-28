# coding=utf-8
from html.parser import HTMLParser

import sys

type = sys.getfilesystemencoding()


# 截止日期
# 每股净资产
# 每股收益
# 每股现金含量
# 每股资本公积金
# 固定资产合计
# 流动资产合计
# 资产总计
# 长期负债合计
# 主营业务收入
# 财务费用
# 净利润
class Stock:
    def __init__(self, line):
        # 20011231,每股净资产,1.5727,每股收益,0.3438,每股现金含量,11,每股资本公积金,0.5289,
        # 固定资产合计,11,流动资产合计,11,资产总计,11,长期负债合计,16,主营业务收入,11,11,净利润,11
        arr = line.split(",")
        self.day = arr[0].replace("-", "") if arr[0] != '-' else '0'
        self.mgzjc = arr[2] if arr[2] != '-' else '0'
        self.mgsy = arr[4] if arr[4] != '-' else '0'
        self.mgxjhl = arr[6] if arr[6] != '-' else '0'
        self.mgjbgjj = arr[8] if arr[8] != '-' else '0'
        self.gdzchj = arr[10] if arr[10] != '-' else '0'
        self.ldzchj = arr[12] if arr[12] != '-' else '0'
        self.zchj = arr[14] if arr[14] != '-' else '0'
        self.cqfzhj = arr[16] if arr[16] != '-' else '0'
        self.zyywsr = arr[18] if arr[18] != '-' else '0'
        self.cwfy = arr[19] if arr[19] != '-' else '0'
        self.jlr = arr[21] if arr[21] != '-' else '0'

    def __repr__(self):
        return """day:%s,mgzjc:%s,mgsy:%s,mgxjhl:%s,mgjbgjj:%s,gdzchj:%s,ldzchj:%s,zchj:%s,
        cqfzhj:%s,zyywsr:%s,cwfy:%s,jlr:%s""" % (self.day, self.mgzjc, self.mgsy, self.mgxjhl,
                                                 self.mgjbgjj, self.gdzchj, self.ldzchj, self.zchj,
                                                 self.cqfzhj, self.zyywsr, self.cwfy, self.jlr)


from lxml import html
import stock.baseinfo.HttpUtil as httpUtil
from bs4 import BeautifulSoup


def get_stock(stock_code):
    url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c" % (
        {'stock_code': stock_code})
    req = httpUtil.doget(url=url)

    soup = BeautifulSoup(req, 'html.parser', fromEncoding="utf-8")  # 文档对象

    need = {}
    sold = []
    sallary = []
    # 类名为xxx而且文本内容为hahaha的div
    for item in soup.find_all('tr'):  # ,string='更多'
        temp = item.find_all('td')
        if (len(temp) == 2):
            if (temp[0].text.find('净利润') != -1):
                sallary.append(temp[1].text.replace(',', '').replace('元', ''))
            if (temp[0].text.find('主营业务收入') != -1):
                sold.append(temp[1].text.replace(',', '').replace('元', ''))
        if (len(sold) > 16): break

    return sold, sallary


def analysis(sallary):
    riseAll = []
    for i in range(4):
        rise1 = (sallary[i] - sallary[i + 4]) / sallary[i + 4] * 100
        rise2 = (sallary[i + 4] - sallary[i + 8]) / sallary[i + 8] * 100
        rise3 = (sallary[i + 8] - sallary[i + 12]) / sallary[i + 12] * 100
        riseAll.append([round(rise1,2), round(rise2,2), round(rise3,2)])
    return riseAll


def getCompanyInfo(stname):
    stname=stname.replace('st','')
    sold, sallary = get_stock(stname)

    sallary = [float(x) for x in sallary]
    flag = 0
    print(stname,'--',sallary)
    if ( sallary[0] > sallary[4] and sallary[4] > sallary[8]
            and sallary[1] > sallary[5] and sallary[5] > sallary[9]):
        flag = 1
    if (flag == 1):
        return analysis(sallary)
    return []


