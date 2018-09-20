#!/usr/bin/env python
# Encoding: UTF-8
import datetime
import os


class Logger(object):
    log_path = ""

    def __init__(self, log_path):  # 类似构造函数
        print(log_path)
        today = datetime.date.today()
        print(os.path.normpath(log_path))
        print(os.path.dirname(log_path))
        # path_end = log_path[-1]
        # if path_end is not '/':
        #     pass
        print(today.strftime('%Y%m'))
        print(today.strftime('%Y%m%d'))
        pass

    def move(self, dx, dy):
        print(self.way_of_reproduction)
        position = [0, 0]
        position[0] = position[0] + dx
        position[1] = position[1] + dy
        return position
