import queue
import threading

'''
qx=init(process)
for i in range(len(listx)):
    produceSinle(qx,listx[i])
'''

# 消费者类
count = []
count.append(0)


# 这里做方法执行的一些包装
def Consumer(q, method):
    while True:
        count[0] += 1
        if (count[0] % 10 == 0):
            print(count[0])
        method(q.get())


# 初始化消费队列,队列大小以及线程个数
def init(method, queueMaxsize=10000, threads=16):
    q = queue.Queue(queueMaxsize)
    for j in range(threads):
        t = threading.Thread(target=Consumer, args=(q, method))
        t.start()
    return q


# 生产的时候把数据放入队列，队里会自动消费(需要初始化init q为初始化的队列)
def produceSinle(q, content):
    if not q.full():
        q.put(content)
        return 0
    else:
        print('queue is full,please enlarge the queue!')
        return 1

