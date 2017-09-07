# encoding: utf-8

s1 = (2, 1.3, 'love', 5.6, 9, 12, False)  # 定值表 也有翻译为元组 tuple
s2 = [True, 5, 'smile']  # 表 list
# tuple和list的主要区别在于，一旦建立，tuple的各个元素不可再变更，而list的各个元素可以再变更。
s3 = [1, [3, 4, 5]]  # 一个序列作为另一个序列的元素
s4 = []  # 空序列

print(s1, type(s1))
print(s2, type(s2))
print(s1[0])
print(s2[2])
print(s3[1][2])

str = 'abcdef123456'
print(str[2:4])

x = range(5)
print x
print len(x)  # 返回： 序列中包含元素的个数
print min(x)  # 返回： 序列中最小的元素
print max(x)  # 返回： 序列中最大的元素
print all(x)  # 返回： True, 如果所有元素都为True的话
print any(x)  # 返回： True, 如果任一元素为True的话
# 下面的方法主要起查询功能，不改变序列本身, 可用于表和定值表:
print sum(x)  # 返回： 序列中所有元素的和
# x为元素值，i为下标(元素在序列中的位置)
print x.count(0)  # 返回： x在s中出现的次数
print x.index(3)  # 返回： x在s中第一次出现的下标
# 由于定值表的元素不可变更，下面方法只适用于表:
l = s3
l2 = s2
l.extend(l2)  # 在表l的末尾添加表l2的所有元素
print l
l.append(x)  # 在l的末尾附加x元素
print l
l.sort()  # 对l中的元素排序
print l
l.reverse()  # 将l中的元素逆序
print l
l.pop()  # 返回：表l的最后一个元素，并在表l中删除该元素
print l
del l[0]  # 删除0下标该元素
print l
# (以上这些方法都是在原来的表的上进行操作，会对原来的表产生影响，而不是返回一个新表。)

# str为一个字符串，sub为str的一个子字符串。s为一个序列，它的元素都是字符串。width为一个整数，用于说明新生成字符串的宽度。
sub = '123456'
s = ['a', 'b', 'c']
print str.count(sub)  # 返回：sub在str中出现的次数
print str.find(sub)  # 返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1
print str.index(sub)  # 返回：从左开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误
print str.rfind(sub)  # 返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，返回 -1
print str.rindex(sub)  # 返回：从右开始，查找sub在str中第一次出现的位置。如果str中不包含sub，举出错误

print str.isalnum()  # 返回：True， 如果所有的字符都是字母或数字
print str.isalpha()  # 返回：True，如果所有的字符都是字母
print str.isdigit()  # 返回：True，如果所有的字符都是数字
print str.istitle()  # 返回：True，如果所有的词的首字母都是大写
print str.isspace()  # 返回：True，如果所有的字符都是空格
print str.islower()  # 返回：True，如果所有的字符都是小写字母
print str.isupper()  # 返回：True，如果所有的字符都是大写字母
print '\n'

# 返回：从左开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.split(',')的方式使用逗号或者其它分割符
# str.split([sep, [max]])
# 返回：从右开始，以空格为分割符(separator)，将str分割为多个子字符串，总共分割max次。将所得的子字符串放在一个表中返回。可以str.rsplit(',')的方式使用逗号或者其它分割符
# str.rsplit([sep, [max]])

print str.join(s)  # 返回：将s中的元素，以str为分割符，合并成为一个字符串。
# 返回：去掉字符串开头和结尾的空格。也可以提供参数sub，去掉位于字符串开头和结尾的sub #str.strip([sub])
print str.strip(sub)
# 返回：用一个新的字符串new_sub替换str中的sub #str.replace(sub, new_sub)
print str.replace(sub, 'new_sub')

print str.capitalize()  # 返回：将str第一个字母大写
print str.lower()  # 返回：将str全部字母改为小写
print str.upper()  # 返回：将str全部字母改为大写
print str.swapcase()  # 返回：将str大写字母改为小写，小写改为大写
print str.title()  # 返回：将str的每个词(以空格分隔)的首字母大写

width = 20
tc = '*'  # 填充字符串
print str.center(width, tc)  # 返回：生成长度为width的字符串，将原字符串放入该字符串中心，其它位置为字符串tc。
print str.ljust(width, tc)  # 返回：生成长度为width的字符串，将原字符串左对齐放入该字符串，其它位置为字符串tc。
print str.rjust(width, tc)  # 返回：生成长度为width的字符串，将原字符串右对齐放入该字符串，其它位置为字符串tc。


print '\n'
# 表推导、、生成表【】为表 list ，append添加内容进表内，下面为简写循环生成内容插入表
L = [x**2 for x in range(10)]
print L

# 同上//多了个判断（聚合列表但是只取用了x值），当y大于10时，对应的同一下标的x进入循环输出到，因为在【】内所以直接添加在表内
xl = [1, 3, 5]
yl = [9, 12, 13]
L = [x**2 for (x, y) in zip(xl, yl) if y > 10]
print L
