import random
import time
import queue
from multiprocessing.managers import BaseManager

# 第一步：建立task_queue 和 result_queue，用来存放任务结果
task_queue = queue.Queue()
result_queue = queue.Queue()



def get_task():
    return task_queue
def get_result():
    return result_queue

class Queuemanager(BaseManager):
    pass

import time
def main(ip,port,kl):
    # 第二步：把创建的两个队列注册在网络上，利用 register 方法，
    # callable参数关联了 Queue 对象，将Queue对象在网络中暴露
    Queuemanager.register('get_task_queue',callable=get_task)
    Queuemanager.register('get_result_queue',callable=get_result)

    # 第三步：初始化对象：绑定IP、端口、设置验证口令 。
    manager = Queuemanager(address=(ip,port),authkey=kl)

    # 第四步：启动管理，监听信息通道
    manager.start()

    # 第五步：通过管理实例的方法获得通过网络访问的Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 第六步：添加任务
    for url in ["ImageUrl_"+str(i) for i in range(10)]:
        print('put task %s ...'%url)
        start = time.time()
        task.put(url)
        end = time.time()
        print('cost:',(end-start))
    # 获得返回结果
    print('try get result...')
    while(True):
        try:
            start = time.time()
            print('result is %s'%result.get(timeout=10))  # 最大等待10秒
            end = time.time()
            print('cost:', (end - start))
        except queue.Empty:
            break
    # 关闭管理
    manager.shutdown()
    print('end')


if __name__ == '__main__':
    ip = '127.0.0.1' # 要绑定的本机IP

    port = 8001 # 端口号

    passwd = b'distributed'  # 口令

    main(ip,port,passwd)
