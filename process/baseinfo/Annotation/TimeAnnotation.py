import time

def isrightTime(timeList):
    time_now = int(time.time())  # unix时间
    time_local = time.localtime(time_now)  # 转换为win_time
    dt = time.strftime("%H:%M", time_local)  # 转换成新的时间格式(18:59:20)
    a = dt.split(':')
    b = []
    for a in dt.split(':'):
        b.append(a)
    c = ''.join(b)
    if (c in timeList and c != timeList[0]):
        return c
    else:
        return '0'


# 定时执行任务
def timer(timeList):
    def actual_decpratpr(function):
        def wrapper(*args, **kwargs):
            result = None
            while (True):
                time.sleep(10)
                currenttime = isrightTime(timeList)
                if currenttime != '0':
                    result = function(*args, **kwargs)
            return result
        return wrapper

    return actual_decpratpr

# @timer(timeList=["1136", "1137", "1134"])
# def foo(x):
#   print(x)
