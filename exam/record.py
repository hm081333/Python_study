# Encoding:UTF-8
record_txt = open('record.txt', 'r')
# 新建名字表
record_name = []
# 新建年龄表
record_age = []
# 新建成绩表
record_score = []
for (index, record) in enumerate(record_txt):
    if (record != '\n'):
        first = record.split(',')
        for (key, second) in enumerate(first):
            if (second.find(' ') != -1):
                second = second[(second.find(' ') + 1): len(second)]
            if (second.find('\n') != -1):
                second = second[0: second.find('\n')]
            if (index > 0):
                if (key == 0):
                    record_name.append(second)
                elif (key == 1):
                    record_age.append(int(second))
                elif (key == 2):
                    record_score.append(int(second))
test1 = '得分低于60的人有 '
for (key, score) in enumerate(record_score):
    if (score < 60):
        test1 += record_name[key] + ' '
print test1.decode('utf-8')

test2 = ''
for (key, name) in enumerate(record_name):
    if (name.find('L') == 0):
        test2 += name + ' '
test2 += '的名字以L开头'
print test2.decode('utf-8')

test3 = '所有人的总分是 ' + str(sum(record_score))
print test3.decode('utf-8')

test4 = '姓名的首字母需要大写，该record.txt是否符合此要求？'
for name in record_name:
    if (name.istitle() != True):
        test4 += ' 不符合 '
    if (name.istitle() == False):
        test4 += name + ' '
test4 += '应该 '
for name in record_name:
    if (name.istitle() == False):
        test4 += name + ' => ' + name.capitalize()
print test4.decode('utf-8')
