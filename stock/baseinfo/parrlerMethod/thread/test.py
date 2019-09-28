import datetime
import numpy as np

x = np.random.rand(1000000)


print(x)
def f(x):
    if x < 0.5:
        return x
    else:
        return x ** 2
begain = datetime.datetime.now()
y = np.full([x.shape[0], 1], np.nan)
for i in range(x.shape[0]):
    y[i] = f(x[1])

end = datetime.datetime.now()
print("For loop cost %s microseconds" % str((end - begain).microseconds))


start = datetime.datetime.now()
#y =[f(ix) for ix in x]
tempx=list(x)
y=[ix for ix in tempx if ix<5]
end = datetime.datetime.now()
print("Loop new in np cost %s microseconds" % str((end - start).microseconds))

# define the function, and loop in np
f = lambda x: x if x < 0.5 else x ** 2.0
start = datetime.datetime.now()
y = np.fromiter((f(xi) for xi in x), x.dtype, count=len(x))
end = datetime.datetime.now()
print("Loop in np cost %s microseconds" % str((end - start).microseconds))

# np.where, pass the value by true or false
start = datetime.datetime.now()
#y = np.where(x < 5, x, x ** 2.0)

#where 得写法优化效果很高，比[x for x in a if x <5]高得多
y = np.where(x < 5)

end = datetime.datetime.now()
print("Np.where cost %s microseconds" % str((end - start).microseconds))

# map the results together,it needs use, but the loop performs in the c-package
# which is better than the loop in python
f = lambda x: x if x < 0.5 else x ** 2.0
start = datetime.datetime.now()
y = list(map(f, x))

end = datetime.datetime.now()
print("Np.map cost %s microseconds" % str((end - start).microseconds))



