# encoding:UTF-8
# 中文
def int(arg):
    arg += 1
    print arg


x = 1
int(x)
print x


def f(x):
    x[0] = 100
    print x


a = [1, 2, 3]
f(a)
print a


x = range(5)
print x
print len(x)
print sum(x)
