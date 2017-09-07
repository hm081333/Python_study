# encoding: UTF-8
def change_integer(a):
    a = a + 1
    return a


# 等于lambda a: a+1
print change_integer(1)


def change_list(b):
    b[0] = b[0] + 1
    return b


print change_list([1, 2, 3])

# 上面是普通生成方法/函数的方法-def
print '\n'
# 下面是快速生成函数的方法-lambda

# 下面例子生成一条： def func(x, y): return x + y ## lambda 传入参数：逻辑返回
func = lambda x, y: x + y
print func(3, 4)
print '\n'


# 函数作为参数传递
# 函数可以作为一个对象，进行参数传递。函数名(比如func)即该对象
def test(f, a, b):
    print f(a, b)


# 普通写法
test(func, 3, 5)
# lambda写法：test((lambda x,y: x + y), 6, 9)
test((lambda x, y: x + y), 3, 5)

# map（）函数 ## 第一个参数是一个函数对象 ## map()将每次从两个表中分别取出一个元素，带入lambda所定义的函数操作数据。
re = map((lambda x, y: x + y), [1, 2, 3], [6, 7, 9])
print re
