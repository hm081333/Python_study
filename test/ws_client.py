#!/usr/bin/env python
# Encoding: UTF-8
import threading
import time
import sys
import os
import signal
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
log_obj = ''
# 日志文件存放路径
log_path = ""
# 是否需要停止运行
need_stop = False


def print_thread():
    # 打印线程信息
    # 全局变量 线程列表
    global thread_list
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
    websocket.dump("thread list", thread_list)
    # print(thread_list)
    # 打印线程状态列表
    websocket.dump("thread state list", thread_state_list)
    # print(thread_state_list)
    # 打印运行中线程数量
    websocket.dump("thread count", threading.activeCount())
    # print("Number of threads:", threading.activeCount())
    pass


# 注册一个进程信号监听事件
def stop_signal_handler(signal_id, frame):
    print("Signal code", signal_id)
    global need_stop
    need_stop = True
    # print('You pressed Ctrl+C!')
    print('Exiting...')
    pass


# 当服务端发来消息时触发
def on_message(ws, message):
    def init():
        print("### Connect successfully ###")
        pass

    def ping():
        print("### Receive Ping successfully ###")
        pass

    def set_config():
        global config
        # noinspection PyBroadException
        try:
            config = json.load(message["data"])
            json.file_dump(config_path, config)
            config_init(False)
            ws.close()
            print("### Set Config successfully ###")
            pass
        except Exception:
            print("### Set Config failure ###")
            pass
        pass

    def send():
        print("### Send successfully ###")
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
        }

        # 在字典中获取对应的方法名
        func = switcher.get(message["type"])
        # 执行方法
        func()
        pass
    except Exception:
        # 不是JSON串，直接打印
        print(message)
        pass
    pass


# 当发生错误时触发
def on_error(ws, error):
    ws.close()
    print(error)
    if debug:
        websocket.dump("threads", threading.enumerate())
        websocket.dump("thread count", threading.activeCount())
        # print(threading.enumerate())
        # print(threading.activeCount())
        pass
    pass


# 当断开连接时触发
def on_close(ws):
    print("### Connection Closed ###")
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
            websocket.dump("thread list", thread_list)
            # print(thread_list)
            # 新建线程追加到线程列表
            thread_list.append(send_thread)
            pass
        send_thread.start()
    except Exception as e:
        print(e)
        pass
    pass


# 签名方法
# 目前是对应DS中functions里面的securityPwd方法
# SECURITY_KEY是DS中的常量，必须与系统中一致
def sign():
    global SECURITY_KEY, PRIVATE_KEY
    md5_obj = hashlib.md5(mac.encode("utf8"))
    mac_md5 = md5_obj.hexdigest()
    md5_obj = hashlib.md5(mac_md5.encode("utf8"))
    md5_obj.update(PRIVATE_KEY.encode("utf8"))
    md5_obj.update(SECURITY_KEY.encode("utf8"))
    return md5_obj.hexdigest()


# 线程运行方法
def run(*args):
    # print(args)
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
            print('Exiting......')
            # 直接退出循环
            break
            pass
        else:
            try:
                # 往服务端发送信息
                ws.send(json_data)
            except Exception as e:
                # 打印发送失败消息
                print(e)
                # 退出死循环
                break
            pass
        pass
    pass
    # 退出死循环，打印
    print("### exit while ###")
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
        header=["x-token:ajKfZgQAf6vIddwC",
                "x-tenant:T001124",
                "x-server:1026"],
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
    里面有ping和pong
    发送ping会开启一条线程...
    '''
    # ws.run_forever(ping_interval=10, ping_timeout=5)
    '''
    运行WebSocket框架的事件循环 
    长连接
    不带ping和pong 
    '''
    ws.run_forever()
    pass


# 重新打开WebSocket连接
def ws_reopen():
    # 打印，证明进入重新连接
    print("### Waiting for %d seconds to reconnect ###" % reconnect_wait)
    # 重新连接等待时间
    time.sleep(reconnect_wait)
    try:
        # 重新连接WebSocket
        ws_open()
        pass
    except Exception as e:
        # 连接失败，打印失败信息
        print(e)
        pass
    pass


# 设置配置参数
def config_init(need_get_config=True):
    # 根据系统类型调取配置文件
    def get():
        global config_path
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
            print("config file not exist")
            return
        # 文件不可读
        if not os.access(config_path, os.R_OK):
            print("config file not readable")
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
            print("### Set Debug successfully ###")
            pass

        def set_host():
            global host
            host = config["host"]
            print("### Set Host successfully ###")
            pass

        def set_reconnect_wait():
            global reconnect_wait
            reconnect_wait = config["reconnectWait"]
            print("### Set Reconnect Wait successfully ###")
            pass

        def set_send_interval():
            global send_interval
            send_interval = config["sendInterval"]
            print("### Set Send Interval successfully ###")
            pass

        def set_security_key():
            global SECURITY_KEY
            SECURITY_KEY = config["securityKey"]
            print("### Set SECURITY KEY successfully ###")
            pass

        def set_private_key():
            global PRIVATE_KEY
            PRIVATE_KEY = config["privateKey"]
            print("### Set PRIVATE KEY successfully ###")
            pass

        def set_log_path():
            global log_path
            log_path = config["logPath"]
            print("### Set Log Path successfully ###")
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


# 主线程开始
if __name__ == "__main__":
    # 调取配置文件 设置配置参数
    config_init()

    if debug:
        # 把目前正在运行的线程赋值给线程列表
        thread_list = threading.enumerate()
        thread_state_list = []
        pass

    # 判断 是否存在第二参数
    if len(sys.argv) >= 2:
        host = sys.argv[1]

    # 使用信号处理模块 停止运行
    # 终端输入了中断字符ctrl+c
    signal.signal(signal.SIGINT, stop_signal_handler)
    # 有kill函数调用产生
    signal.signal(signal.SIGTERM, stop_signal_handler)
    # 尝试连接WebSocket
    ws_open()
    pass
