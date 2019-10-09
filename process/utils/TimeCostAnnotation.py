import time

'''
耗时统计
'''


# 定时执行任务
def timerCost():
    def actual_decpratpr(function):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            print(function.__name__,'cost:',end-start)
            return result
        return wrapper
    return actual_decpratpr


