def year():
    y = input("please input year: ")
    a = y % 400
    b = y % 4
    if not a:
        print("%d is  leap year" % y)
    elif b:
        print("%d is not leap year" % y)
    else:
        print("%d is leap year" % y)


def day():
    day = input("please input date(like:'20080101'):")
    days = 0
    m2 = [2, 4, 6, 9, 11]
    y = int(day[:4])
    m = int(day[4:6])
    d = int(day[6:])
    if (y != 2008):
        print('The year must be 2008')
    for i in range(1, m):
        days += 31
        if (i in m2):
            days -= 1
    else:
        days += d
        print("%s is the first %d days of %d" % (day, days, y))


###################################################################


def modify(j):
    for n, i in enumerate(j):
        if not i:
            continue
        linse = list(open("record.txt", 'r+'))
        linse[n] = linse[n][0].upper() + linse[n][1:]
    fp = open("record.txt", 'w+')
    fp.writelines(linse)
    fp.close()


def record():
    F = []
    L = []
    N = []
    O = 0
    j = []
    flag = False
    fp = open("record.txt", 'r+')
    for eachLine in fp:
        if (eachLine[0] == '#'):
            j.append(0)
            continue
        eachLine.strip()
        if (int(eachLine[-3:]) < 60):
            F.append(eachLine.split(',')[0])
        if (eachLine[0] == 'L'):
            L.append(eachLine.split(',')[0])
        if (ord(eachLine[0]) > 90):
            N.append(eachLine.split(',')[0])
            j.append(1)
            flag = True
        else:
            j.append(0)
        O += int(eachLine[-3:])
    fp.close()
    print("Score below 60 who have: %s" % F)
    print("Names beginning with 'L' to include: %s" % L)
    print("The total score for all: %d" % O)
    if flag:
        modify(j)
        print("Not capitalized initials: %s, already edited." % N)


if __name__ == '__main__':
    # year()
    day()
    # record()
