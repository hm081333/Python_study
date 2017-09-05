# Encoding: UTF-8
from ly import zhcn  # 引用打印中文的方法
import os  # 引用操作系统的库
import re  # 引用正则库
import datetime  # 引用日期操作库

filename = "output_1981.10.21.txt"
regular = "(?P<qianzhui>.*)[_](?P<year>\d{4}).(?P<month>[0-1]\d).(?P<day>[0-3]\d).(?P<file>.*)"
tf = re.match(regular, filename)
if (tf == None):
    zhcn('文件名输入错误')
    exit()
get_time = re.search(regular, filename)
year = get_time.group("year")
month = get_time.group("month")
day = get_time.group("day")
file = get_time.group("file")
date = datetime.date(int(2017), int(8), int(27))
wd = date.weekday() + 1
os.rename(filename, "output_" + year + "-" + month + "-" + day + "-" + str(wd) + ".txt")
