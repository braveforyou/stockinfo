import json
import pandas as pd
import os


# 获取文件夹内所有文档的内容
def getDirContens(DIR):
    contents = [loadJsonFile(os.path.join(DIR, f)) for f in os.listdir(DIR)]
    return contents



def getDirStringContens(DIR):
    contents = [loadString(os.path.join(DIR, f)) for f in os.listdir(DIR)]
    return contents


def getDirFileName(DIR):
    files = [os.path.join(DIR, f) for f in os.listdir(DIR)]
    return files


# +++++++++++ 读文件 ++++++++++++++++++++

# 读Json，返回dict
def loadJsonFile(filename):
    with open(filename, 'r') as load_f:
        load_dict = json.load(load_f)
        return load_dict


# 读txt，返回全文
def loadString(fileName):  # general function to parse tab -delimited floats
    result = ""
    fr = open(fileName, encoding='utf-8')
    for line in fr.readlines():
        line = line.replace('\n', '')
        result = result + line + " "
    return result


# 读txt，返回全文
def loadTxt(fileName):  # general function to parse tab -delimited floats
    dataMat = []
    fr = open(fileName, encoding='utf-8')
    for line in fr.readlines():
        line = line.replace('\n', '')
        dataMat.append(line)
    return dataMat


# 读csv文件，返回dataframe
def loadCsv(fileName):
    dataframe = pd.read_csv(fileName)
    return dataframe


# ++++++++++++写文件++++++++++++++

def writeCsv(fileName, dataFrame, index=False):
    dataFrame.to_csv(fileName, index=index)
    return ""



def writeListTxt(fileName, content, huanhang=False):
    fl = open(fileName, 'a', encoding='utf-8')
    warn = 0
    count = 0
    for item in content:
        count += 1
        try:
            if (count != len(content)):
                fl.write(str(item) + ",")
            else:
                fl.write(str(item))
            if (huanhang):
                fl.write("\n")
        except:
            raise
            warn += 1
    fl.write("\n")
    fl.close()
    return ""


def writeArrayTxt(fileName, content, huanhang=False):
    fl = open(fileName, 'a', encoding='utf-8')
    warn = 0
    for item in content:
        tempx = ""
        for inner in item:
            tempx += str(inner) + ","
        tempx = tempx[0:len(tempx) - 1]
        try:
            fl.write(tempx)
            if (huanhang):
                fl.write("\n")
        except:
            warn += 1
    fl.close()
    return ""


def writeStringTxt(fileName, content, huanhang=False, overWrite=False):
    if (os.path.exists(fileName) == True and overWrite == False): return
    fl = open(fileName, 'a')
    try:
        fl.write(content)
        if (huanhang):
            fl.write("\n")
    except:
        raise
        warn += 1
    fl.close()
    return ""


# ++++++++++++++++++++++++++++++++++++++++++++++++++

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
