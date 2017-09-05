# Encoding: UTF-8
# time库的练习--时间与日期
from ly import zhcn
import time  # 时间库
import datetime  # 日期库

# print(dir(time))#打印time模块含有的方法对象
# print(dir(datetime))#打印datetime模块含有的方法对象

print time.time()  # 时间戳
# print time.clock()  # 进程执行时间-耗时

# print('休眠')
# time.sleep(10)     # 休眠十秒
# print('唤醒')

# print time.gmtime()      # 返回struct_time格式的UTC时间
print time.localtime()   # 返回struct_time格式的当地时间, 当地时区根据系统环境决定。
# print time.mktime()      # 将struct_time格式转换成wall clock time  会报错。。原因不明

t = datetime.datetime(2012, 9, 3, 21, 30)
t_next = datetime.datetime(2012, 9, 5, 23, 30)
delta1 = datetime.timedelta(seconds=600)  # 时间间隔
delta2 = datetime.timedelta(weeks=3)  # 时间间隔
print(t + delta1)  # t时间加上间隔600秒后的时间
print(t + delta2)  # t时间加上间隔3周后的时间
print(t_next - t)  # t_next时间减去t时间得出t_next与t的间隔

# from datetime import datetime  # datetime库里的datetime对象
# print(dir(datetime.datetime))  # 打印datetime模块里面datetime对象含有的方法对象

format = "output-%Y-%m-%d-%H%M%S.txt"  # 格式
str = "output-1997-12-23-030000.txt"  # 文件名
t = datetime.datetime.strptime(str, format)  # 根据格式在文件名中提取日期
print t
print(t_next.strftime(format))  # 根据格式把日期格式化为文件名
