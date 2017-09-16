# Encoding: UTF-8
import glob

# dir查看类对象中所有方法
# print dir(glob.glob)

print(glob.glob('D:\\PY\\lib\\*'))

for x in glob.glob('D:\\PY\\lib\\*'):
    print x
    # print '\n'
    pass
