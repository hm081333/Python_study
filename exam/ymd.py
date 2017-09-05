# Encoding: UTF-8
# 打印中文
def zhcn(string):
	print string.decode('utf-8')

# 判断闰年方法
def year(year):
	# year = raw_input()
	if year == 'exit':
		exit()
	elif len(str(year)) != 4 or year.isdigit() == False:
		zhcn('请正确输入4位数的年份\n')
		return False
	year = int(year)
	if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
		zhcn(str(year) + '年是闰年')
		return 29
	else:
		zhcn(str(year) + '年不是闰年')
		return 28

# 判断日期是第几天方法
def date():
	if date == 'exit':
		exit()
	elif len(str(date)) != 8 or date.isdigit() == False:
		zhcn('请正确输入8位数的日期（如：20170820）')
	# big_month = [1,3,5,7,8,10,12]
	# small_month = [2,4,6,9,11]
	year_month = [31,28,31,30,31,30,31,31,30,31,30,31]
	year = int(date[0 : 4])
	if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
		year_month[1] = 29
	month = int(date[4 : 6])
	day = int(date[6 : 8])
	now_day = 0;
	for d in range(0, month - 1):
		now_day += year_month[d]
	now_day += day
	zhcn(str(year) + '年的第' + str(now_day) + '天')

# while 1:
# 	zhcn('请输入你要验证的年份（四位数）：')
# 	rs = year(raw_input())
# 	if rs:
# 		break
# 	pass

while 1:
	zhcn('请输入8位数日期（如：20170820）：')
	rs = date(raw_input())
	if rs:
		break
	pass
