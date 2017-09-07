# encoding:utf-8
# coding=utf8
cs = 0
xx = 0
record_list = [[], [], []]
name = []
age = []
score = []
for i in open('record.txt', 'r'):  # 打开文件这个循环对象并自动for循环
    i = i.split(',')  # 拆分字符串为表list，类似PHP的explode(',',$str)拆分字符串为数组
    for x in i:  # 处理拆分后的表的数据
        if (x == '\n'):  # 跳过空行
            xx += 1
            cs = 0
            continue
        if ((x.find('#')) != -1):  # 已知井号在前面
            where = x.find('#') + 1
            x = x[where:]
        if ((x.find(' ')) != -1):  # 已知有些值前面有空格
            where = x.find(' ') + 1
            x = x[where:]
        if ((x.find('\n')) != -1):  # 已知每行结尾有换行
            end = x.find('\n')
            x = x[0:end]
        if (xx > 0):
            if cs == 0:
                name.append(x)
            elif cs == 1:
                age.append(int(x))  # 年龄是数字
            elif cs == 2:
                score.append(int(x))  # 成绩是数字
        else:
            record_list[cs] = [x]
        cs += 1

record_list[0].extend(name)
record_list[1].extend(age)
record_list[2].extend(score)
print(record_list)
print(name, age, score)

q1 = '得分低于60的人都有谁？'
print q1
# enumerate函数将一个可遍历的数据对象组合为一个索引序列，同时列出数据和下标
for (key, item) in enumerate(score):
    if (item < 60):
        print name[key]

q2 = '谁的名字以L开头？'
print q2
for a in name:
    if ((a.find('L')) != -1):
        print a

q3 = '所有人的总分是多少?'
print q3
print str(sum(score)) + '分'

q4 = '姓名的首字母需要大写，该record.txt是否符合此要求？ 如何纠正错误的地方？'
print q4
for (key, item) in enumerate(name):
    if (item.istitle() == False):
        print '该record.txt不符合此要求'
        print name[key] + ' 首字母没有大写'
        print '纠正：把 ' + name[key] + ' 改为 ' + name[key].capitalize()
        name[key] = name[key].capitalize()
        record_list[0][key + 1] = record_list[0][key + 1].capitalize()

print(record_list)
print (name, age, score)
