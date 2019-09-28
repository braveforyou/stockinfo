import queue
import threading
import time


class ProduceConsumer:
    count = 0
    method = []
    que = []
    maxsize = 0

    # 初始化消费队列,队列大小以及线程个数
    def __init__(self, consumeMethod, queueMaxsize=100, threads=6, maxsize=-1):
        self.que = queue.Queue(queueMaxsize)
        self.maxsize = maxsize
        for j in range(threads):
            t = threading.Thread(target=self.Consumer, args=(self.que, consumeMethod))
            t.start()

    def Consumer(self, q, method):
        while True:
            try:
                self.count += 1
                if (self.maxsize!=-1 and self.count == self.maxsize - 1):
                    print('end')
                    break
                print('Consumer Count:',self.count,'qsize:',self.que.qsize())
                method(q.get())
            except:
                raise
                1
    # 生产的时候把数据放入队列，队里会自动消费(需要初始化init q为初始化的队列)
    def produceSinle(self, content):
        if not self.que.full():
            self.que.put(content)
            return 0
        else:
            print('queue is full!')
            return 1


'''
需要配合，在produce满了的情况下sleep一会
def printContent(x):
    1
newempl = Employee(printContent)

for i in range(2000):
    if (newempl.produceSinle(i) == 1):
        time.sleep(0.1)
'''
