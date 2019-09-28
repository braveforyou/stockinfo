import requests
import json


def dopost(url, dictContent):
    headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    response = requests.post(url, data=json.dumps(dictContent), headers=headers)
    return response.text


def doget(url, paramDict={}):
    content = ""
    for key in paramDict.keys():
        content += key + "=" + str(paramDict[key]) + "&"
    content = content[:len(content) - 1]
    url += content
    res = requests.get(url,'utf-8')  # 直接产生get请求
    return res.content # 打印返回结果
