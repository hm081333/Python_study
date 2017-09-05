# Encoding: UTF-8
i = ['a','b','c']
l = [1,2,3]
print dict(zip(i,l))

l1=[1,2,3,6,87,3]
l2=['aa','bb','cc','dd','ee','ff']
d={}
for index in range(len(l1)):
    d[l1[index]]=l2[index] # 注意，key 若重复，则新值覆盖旧值 
print d