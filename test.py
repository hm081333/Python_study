# encoding: utf-8
# len(S)为字符串总长度
# 间隔两个取一个值
S = 'abcdefghijk'
for i in range(0, len(S), 2):
    print S[i]
print '\n'

# 利用enumerate()函数，可以在每次循环中同时得到下标和元素：
for (index, char) in enumerate(S):
    print index
    print char
print '\n'

# zip()函数的功能，就是从多个列表中，依次各取出一个元素。每次取出的(来自不同列表的)元素合成一个元组，合并成的元组放入zip()返回的列表中。zip()函数起到了聚合列表的功能。

ta = [1, 2, 3]
tb = [9, 8, 7]
tc = ['a', 'b', 'c']
for (a, b, c) in zip(ta, tb, tc):
    print(a, b, c)
print '\n'

# 聚合分解聚合例子
# cluster
# 聚合列表
zipped = zip(ta, tb, tc)
print(zipped)

# decompose
# 分解聚合
na, nb, nc = zip(*zipped)
print(na, nb, nc)

print '\n'

# 打开文件，读取文件内容==循环对象、、open()返回的实际上是一个循环对象，包含有next()方法
for line in open('test.txt'):
    print line
print '\n'


# 生成循环对象 yield为暂停，编译后需要调用next()继续下一步
# 生成器(generator)的主要目的是构成一个用户自定义的循环对象。
# 生成器中可以有多个yield。当生成器遇到一个yield时，会暂停运行生成器，返回yield后面的值。当再次调用生成器的时候，会从刚才暂停的地方继续运行，直到下一个yield。生成器自身又构成一个循环器，每次循环使用一个yield返回的值。
def gen():
    a = 100
    yield a
    a = a * 8
    yield a
    yield 1000


# for解开循环对象
for i in gen():
    print i
print '\n'


def gen():
    for i in range(4):
        yield i


# for解开循环对象
for i in gen():
    print i
print '\n'

# 生成器表达式(Generator Expression)跟上面的def一样，生成一个循环对象
G = (x for x in range(4))
# for解开循环对象
for i in gen():
    print i
print '\n'

# 表推导、、生成表【】为表 list ，append添加内容进表内，下面为简写循环生成内容插入表
L = [x**2 for x in range(10)]
print L
print '\n'

# 同上//多了个判断（聚合列表但是只取用了x值），当y大于10时，对应的同一下标的x进入循环输出到，因为在【】内所以直接添加在表内
xl = [1, 3, 5]
yl = [9, 12, 13]
L = [x**2 for (x, y) in zip(xl, yl) if y > 10]
print L

i = ['a','b','c']
l = [1,2,3]
print dict(zip(i,l))

l1=[1,2,3,6,87,3]
l2=['aa','bb','cc','dd','ee','ff']
d={}
for index in range(len(l1)):
    d[l1[index]]=l2[index] # 注意，key 若重复，则新值覆盖旧值 
print d
