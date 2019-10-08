import numpy as np

def yanghui(Step=3):

    result=list(np.zeros(Step))

    if(Step==1):
        return [1]
    elif(Step==2):
        return [1,1]
    else:
        temp=yanghui(Step-1)
        result[0]=1
        result[-1]=1
        for i in range(len(result)):
            if(i==0 or i==len(result)-1):continue
            result[i]=temp[i-1]+temp[i]
        return result


def fib(max):
    n=1
    while n < max:
        yield yanghui(n)
        n = n + 1
    return 'done'



x=fib(10)
print(next(x))
print(next(x))
print(next(x))
print(next(x))
print(next(x))
print(next(x))

from functools import reduce

data=[1,2,3,2,4,1,2]
temp=reduce(lambda x,y:x*y,data)
print(temp)