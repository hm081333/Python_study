#!/usr/bin/env python
# Encoding: UTF-8


class GetMac(object):
    mac = ""

    def __init__(self,
                 upper=False,
                 lower=False,
                 colon=False
                 ):  # 类似构造函数
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        if (upper):
            mac = mac.upper()
            pass
        elif lower:
            mac = mac.lower()
            pass

        if colon:
            old_mac = mac
            mac = ""
            for index, char in enumerate(old_mac):
                mac += char
                if index % 2:
                    mac += ":"
                    pass
                pass
            mac = mac[0:-1]
            pass
        else:
            mac = mac.replace(":", "")
            pass

        self.mac = mac
        pass

    pass


class Json(object):
    import json as json_module
    debug = False

    def __init__(self, debug=False):  # 类似构造函数
        self.debug = debug
        pass

    def load(self, json_str):
        return self.json_module.loads(json_str)
        pass

    def file_load(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return self.json_module.load(f)
                pass
            pass
        except Exception as e:
            print("fail to read file")
            print(e)
            pass
        pass

    def dump(self, obj):
        return self.json_module.dumps(obj)
        pass

    def file_dump(self, file_path, obj):
        try:
            with open(file_path, 'w') as f:
                self.json_module.dump(obj, f)
                pass
            pass
        except Exception as e:
            print("fail to write file")
            print(e)
            pass
        pass

    pass


class Logger(object):
    import logging
    from logging import handlers
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = self.logging.getLogger(filename)
        format_str = self.logging.Formatter(fmt)  # 设置日志格式
        # format_str = self.logging.Formatter(fmt, '%Y-%m-%d %H:%M:%S')  # 设置日志格式
        self.logger.setLevel(self.levels.get(level))  # 设置日志级别
        sh = self.logging.StreamHandler()  # 往屏幕上输出
        # sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = self.handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)
        self.logger.dump = self.dump
        self.logger.crit = self.logger.critical
        pass

    def dump(self, level, title, msg, *args, **kwargs):
        level = self.levels.get(level)
        self.logger._log(level, "--- " + title + " ---", args, **kwargs)
        self.logger._log(level, msg, args, **kwargs)
        self.logger._log(level, "-----------------------", args, **kwargs)
        pass
