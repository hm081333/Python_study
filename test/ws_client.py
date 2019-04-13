#!/usr/bin/env python
# Encoding: UTF-8
import argparse
import os
import signal
import sys
import threading
import time

from module.module import *

try:
    # 尝试引入WebSocket库
    import websocket
except ImportError:
    # 引入失败
    try:
        # 执行安装WebSocket库命令
        os.system("pip install websocket-client || easy_install websocket-client")
        pass
    except OSError:
        # 安装失败
        print("Unable to install websocket-client library! Exit!")
        # 退出
        sys.exit(1)
        pass
    import websocket

    pass

try:
    # 尝试引入hashlib库 用于md5
    import hashlib
except ImportError:
    # 引入失败
    try:
        # 执行安装hashlib库命令
        os.system("pip install hashlib || easy_install hashlib")
        pass
    except OSError:
        # 安装失败
        print("Unable to install hashlib library! Exit!")
        # 退出
        sys.exit(1)
        pass
    import hashlib

    pass

# 程序当前版本
version = "1.0.1"
# 当前版本 构建日期
build_date = "20180928"
# 实例化json类
json = Json()
# 全局配置信息 默认空
config = {}
# 默认请求地址
host = "ws://192.168.1.135:7272/"
# md5默认密钥
SECURITY_KEY = "4329098asdkae"
# 设备私钥
PRIVATE_KEY = ""
# 是否开启调试模式标识
debug = False
# 断线等待重连时间
reconnect_wait = 10
# 发送心跳间隔
send_interval = 5
# 设备网卡MAC地址
mac = GetMac(upper=True, colon=True).mac
# 配置文件存放路径
config_path = ""
# 初始化日志写入 对象
# log_obj = {}
# 日志文件存放路径
log_path = ""
# 是否需要停止运行
need_stop = False
# 线程列表
thread_list = []
# 线程状态列表
thread_state_list = []


def print_thread():
    # 打印线程信息
    # 全局变量 线程列表
    global thread_list, thread_state_list
    # 循环线程列表
    for index, thread in enumerate(thread_list):
        # noinspection PyBroadException
        try:
            # 当前循环 线程 状态已经存在线程状态列表内，替换状态
            thread_state_list[index] = thread.isAlive()
            pass
        except Exception:
            # 往线程列表追加新线程的状态
            thread_state_list.append(thread.isAlive())
            pass
        pass
    # 打印线程列表
    log_obj.dump("debug", "thread list", thread_list)
    # 打印线程状态列表
    log_obj.dump("debug", "thread state list", thread_state_list)
    # 打印运行中线程数量
    log_obj.dump("debug", "thread count", threading.activeCount())
    pass


# 注册一个进程信号监听事件
def stop_signal_handler(signal_id, frame):
    if debug:
        log_obj.debug("Signal code " + signal_id)
        log_obj.debug(frame)
        pass

    global need_stop
    need_stop = True
    # print('You pressed Ctrl+C!')
    log_obj.info("Exiting...")
    pass


# 当服务端发来消息时触发
def on_message(ws, message):
    def init():
        log_obj.info("### Connect successfully ###")
        pass

    def ping():
        log_obj.info("### Receive Ping successfully ###")
        pass

    def set_config():
        global config
        # noinspection PyBroadException
        try:
            # 服务器下发配置
            new_config = message["data"]
            # 合并配置
            config.update(new_config)
            json.file_dump(config_path, config)
            config_init(False)
            ws.close()
            log_obj.info("### Set Config successfully ###")
            pass
        except Exception:
            log_obj.error("### Set Config failure ###")
            pass
        pass

    def send():
        log_obj.info("### Send successfully ###")
        pass

    def upgrade():
        log_obj.info("### Upgrade successfully ###")
        pass

    # try except 判断返回是否json传
    # noinspection PyBroadException
    try:
        # JSON串转字典
        message = json.load(message)
        # 构造字典 等同switch case
        switcher = {
            "init": init,
            "ping": ping,
            "send": send,
            "config": set_config,
            "upgrade": upgrade,
        }

        # 在字典中获取对应的方法名
        func = switcher.get(message["type"])
        # 执行方法
        func()
        pass
    except Exception:
        # 不是JSON串，直接打印
        log_obj.error(message)
        pass
    pass


# 当发生错误时触发
def on_error(ws, error):
    ws.close()
    log_obj.error(error)
    if debug:
        log_obj.dump("debug", "current threads", threading.enumerate())
        log_obj.dump("debug", "current thread count", threading.activeCount())
        pass
    pass


# 当断开连接时触发
def on_close(ws):
    log_obj.info("### Connection Closed ###")
    ws.close()
    if not need_stop:
        # 重新打开WebSocket连接
        ws_reopen()
        pass
    pass


# 当连接成功时触发
def on_open(ws):
    # 开启一个线程 调用run方法
    try:
        # 新建一个线程，运行run方法，ws以参数传入，线程名为send_thread
        send_thread = threading.Thread(target=run, args=(ws,), name="send_thread")
        # 设为Daemon线程
        send_thread.setDaemon(True)
        if debug:
            global thread_list
            log_obj.dump("debug", "thread list", thread_list)
            # 新建线程追加到线程列表
            thread_list.append(send_thread)
            pass
        send_thread.start()
    except Exception as te:
        log_obj.error(te)
        pass
    pass


# 签名方法
# 目前是对应DS中functions里面的securityPwd方法
# SECURITY_KEY是DS中的常量，必须与系统中一致
def sign(sign_str=mac):
    global SECURITY_KEY, PRIVATE_KEY
    # 先 加密待加密字符串
    md5_obj = hashlib.md5(sign_str.encode("utf8"))
    sign_str_md5 = md5_obj.hexdigest()
    # 拼接 盐 和 密钥 加密
    md5_obj = hashlib.md5(sign_str_md5.encode("utf8"))
    md5_obj.update(PRIVATE_KEY.encode("utf8"))
    md5_obj.update(SECURITY_KEY.encode("utf8"))
    return md5_obj.hexdigest()


# 线程运行方法
def run(*args):
    ws = args[0]
    # 要发送的信息列表
    data = {
        'ping': mac,
        'sign': sign()
    }
    # 列表转JSON
    json_data = json.dump(data)
    while True:
        if debug:
            # 打印线程信息
            print_thread()
            pass
        # 休眠5秒，不计算失败情况下，等于5秒发送一次
        time.sleep(send_interval)
        # 将要关闭
        if need_stop:
            log_obj.info("Exiting......")
            # 直接退出循环
            break
            pass
        else:
            try:
                # 往服务端发送信息
                ws.send(json_data)
            except Exception as re:
                # 打印发送失败消息
                log_obj.error(re)
                # 退出死循环
                break
            pass
        pass
    pass
    # 退出死循环，打印
    log_obj.info("### exit while ###")
    # 主动断开WebSocket连接
    ws.close()
    pass


# 打开WebSocket连接
def ws_open():
    # 启用跟踪器 开启后会打印 所有 请求相关信息
    websocket.enableTrace(debug)
    # 新建WebSocket连接
    ws = websocket.WebSocketApp(
        # WebSocket地址
        host,
        # 追加header
        # header=["x-token:ajKfZgQAf6vIddwC",
        #         "x-tenant:T001124",
        #         "x-server:1026"],
        # 打开WebSocket后的回调def
        on_open=on_open,
        # 收到消息时回调
        on_message=on_message,
        # 发生错误时回调
        on_error=on_error,
        # 断开连接时回调
        on_close=on_close
    )
    '''
    运行WebSocket框架的事件循环 
    长连接
    '''
    try:
        ws.run_forever()
        pass
    except Exception as wre:
        log_obj.error(wre)
        pass
    pass


# 重新打开WebSocket连接
def ws_reopen():
    # 打印，证明进入重新连接
    log_obj.info("### Waiting for %d seconds to reconnect ###" % reconnect_wait)
    # 重新连接等待时间
    time.sleep(reconnect_wait)
    try:
        # 重新连接WebSocket
        ws_open()
        pass
    except Exception as oe:
        # 连接失败，打印失败信息
        log_obj.error(oe)
        pass
    pass


# 设置配置参数
def config_init(need_get_config=True):
    # 根据系统类型调取配置文件
    def get():
        # 没有配置文件路径
        global config_path
        if not config_path:
            # win32系统 = windows
            if sys.platform == 'win32':
                # 文件当前路径
                current_path = os.path.dirname(os.path.realpath(__file__))
                # windows下配置文件存放在同一目录
                config_path = current_path + os.path.sep + "config.json"
                pass
            else:
                # Linux上配置文件规定存放在/etc/miner
                config_path = "/etc/miner/config.json"
                pass
            pass
        # 读取文件获取配置信息
        get_config()
        pass

    # 读取文件获取配置信息
    def get_config():
        global config_path
        # os.F_OK: 检查文件是否存在;
        # os.R_OK: 检查文件是否可读;
        # os.W_OK: 检查文件是否可以写入;
        # os.X_OK: 检查文件是否可以执行
        # 文件不存在
        if not os.access(config_path, os.F_OK):
            log_obj.error("config file not exist")
            return
        # 文件不可读
        if not os.access(config_path, os.R_OK):
            log_obj.error("config file not readable")
            return
        global config
        config = json.file_load(config_path)
        pass

    # 根据读取出的配置设置参数
    def set_config():
        global config

        def set_debug():
            global debug
            debug = config["debug"]
            log_obj.info("### Set Debug successfully ###")
            pass

        def set_host():
            global host
            host = config["host"]
            log_obj.info("### Set Host successfully ###")
            pass

        def set_reconnect_wait():
            global reconnect_wait
            reconnect_wait = config["reconnectWait"]
            log_obj.info("### Set Reconnect Wait successfully ###")
            pass

        def set_send_interval():
            global send_interval
            send_interval = config["sendInterval"]
            log_obj.info("### Set Send Interval successfully ###")
            pass

        def set_security_key():
            global SECURITY_KEY
            SECURITY_KEY = config["securityKey"]
            log_obj.info("### Set SECURITY KEY successfully ###")
            pass

        def set_private_key():
            global PRIVATE_KEY
            PRIVATE_KEY = config["privateKey"]
            log_obj.info("### Set PRIVATE KEY successfully ###")
            pass

        def set_log_path():
            global log_path
            log_path = config["logPath"]
            log_obj.info("### Set Log Path successfully ###")
            pass

        # 构造字典 等同switch case
        switcher = {
            "debug": set_debug,
            "host": set_host,
            "reconnectWait": set_reconnect_wait,
            "sendInterval": set_send_interval,
            "securityKey": set_security_key,
            "privateKey": set_private_key,
            "logPath": set_log_path,
        }
        # 循环出key值并赋值
        for configKey in config:
            # 在字典中获取对应的方法名
            func = switcher.get(configKey)
            # 执行方法
            func()
            pass
        pass

    if need_get_config:
        get()
    set_config()
    pass


# 构建传入参数解析
def parse_args():
    # 创建一个解析对象
    parser = argparse.ArgumentParser(
        # 程序名
        prog="Miner",
        # help时显示的开始文字
        description="A unified platform for miners.",
        # help时显示的结尾文字
        epilog="If you have more questions, please contact the developer.",
        # 是否增加-h/--help选项
        add_help=True,
    )
    # 向该对象中添加你要关注的命令行参数和选项
    parser.add_argument(
        # 必选，指定参数的形式，一般写两个，一个短参数，一个长参数
        # 不写横杠就是argv形式
        "-u",
        "--url",
        # 指定这个参数后面的value有多少个
        # +表示至少一个 ?表示一个或0个 *表示0个或多个
        # nargs='?',
        # 如果命令行没有出现这个选项，那么使用default指定的默认值
        # default=0,
        # 如果希望传进来的参数是指定的类型（例如 float, int or file等可以从字符串转化过来的类型），可以使用
        # type=int,
        # 设置参数值的范围，如果choices中的类型不是字符串，记得指定type哦
        # choices=['a', 'b', 'd'],
        # 通常选项是可选的，但是如果required=True那么就是必须的了
        # required=True,
        # 参数的名字，在显示 帮助信息时才用到
        # metavar="ws_url",
        # 设置这个选项的值就是解析出来后放到哪个属性中
        # dest="host",
        # 操作类型，常量 无需填入参数，默认为false，使用参数时为true
        # action="store_true",
        # 设置这个选项的帮助信息
        help="websocket url. ex. ws://127.0.0.1:7272/"
    )
    parser.add_argument(
        "-config",
        help="Config file for Miner."
    )
    parser.add_argument(
        "-v",
        "-version",
        "--version",
        # 操作类型，版本号，打印后会自动退出程序
        action="version",
        # 打印的信息
        version="%(prog)s" + "\tv" + version + "\tBuilt\ton\t" + build_date,
        help="Show current version of Miner."
    )

    # 返回解析参数
    return parser.parse_args()


def main():
    # 初始化日志方法 生成日志对象
    global log_obj
    log_obj = logger()
    # 获取传入参数
    args = parse_args()
    # 判断 是否自定义配置文件路径
    if args.config:
        global config_path
        config_path = args.config
        # 文件不存在 或 不可读
        if not os.access(config_path, os.F_OK) or not os.access(config_path, os.R_OK):
            log_obj.error("config file is not exist or not readable")
            # 终止运行程序
            sys.exit(2)
            pass
        pass

    # 调取配置文件 设置配置参数
    config_init()

    # 判断 是否自定义地址
    if args.url:
        global host
        host = args.url
        pass

    if debug:
        global thread_list, thread_state_list
        # 把目前正在运行的线程赋值给线程列表
        thread_list = threading.enumerate()
        thread_state_list = []
        pass

    # 尝试连接WebSocket
    ws_open()

    pass


# 构造日志方法
def logger():
    # win32系统 = windows
    if sys.platform == 'win32':
        # 文件当前路径
        current_path = os.path.dirname(os.path.realpath(__file__))
        # windows下配置文件存放在同一目录
        logger_path = current_path + os.path.sep + "miner.log"
        pass
    else:
        # Linux上日志文件规定存放在/var/log/miner
        logger_path = "/var/log/miner/miner.log"
        pass
    # fmt = '%(asctime)s - %(module)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    fmt = '%(asctime)s|%(levelname)s|%(module)s|%(lineno)d|%(message)s'
    return Logger(logger_path, level='debug', fmt=fmt).logger
    # return Logger(logger_path, level='debug', fmt=fmt)


# 主线程开始
if __name__ == "__main__":
    # 使用信号处理模块 停止运行
    # 终端输入了中断字符ctrl+c
    signal.signal(signal.SIGINT, stop_signal_handler)
    # 有kill函数调用产生
    signal.signal(signal.SIGTERM, stop_signal_handler)

    try:
        main()
        pass
    except Exception as e:
        log_obj.error(e)
        pass

    pass
