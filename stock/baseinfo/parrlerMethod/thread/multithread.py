from multiprocessing import Pool, Queue
import os, time, random

'''
进程锁可以避免因为多个进程访问共享资源而发生冲突，这里的共享资源不是像多线程中那样的全局变量，上面已经说了普通的全局变量不会
在进程间共享，而是系统中的文件或者console输出这类系统的资源，还有特别的能在进程间通信的共享内存资源，这些能被进程竞争。
这里以文件为例，因为同一时间，只能有一个进程，对文件进行写入操作，这是操作系统的设定。同时由操作系统随机决定哪个进程来写入操作
'''

#用process 和Queue是可以进行结果缓存得



def long_time_task(name):
    try:
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    except:
        print('!!!!!!!!!!!!!!!!!!!!!')



if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p=Pool(4)
    for i in range(5):
        x = p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

