#!/usr/bin/env python
# encoding: utf-8
import threading
import time
import sys
import os
import uuid
import json

try:
    # 尝试引入websocket库
    import websocket
except ImportError:
    # 引入失败
    try:
        # 安装websocket库命令
        command_to_execute = "pip install websocket-client || easy_install websocket-client"
        # 执行安装命令
        os.system(command_to_execute)
    except OSError:
        # 安装失败
        print("Unable to install websocket-client library! Exit!")
        # 退出
        sys.exit(1)
    import websocket

try:
    # 尝试引入hashlib库
    import hashlib
except ImportError:
    # 引入失败
    try:
        # 安装hashlib库命令
        command_to_execute = "pip install hashlib || easy_install hashlib"
        # 执行安装命令
        os.system(command_to_execute)
    except OSError:
        # 安装失败
        print("Unable to install hashlib library! Exit!")
        # 退出
        sys.exit(1)
    import hashlib

thread_list = threading.enumerate()
thread_state_list = []
# 断线等待重连时间
reconnect_wait = 5
# 服务端识别的终端ID
client_id = ""


# 获取机器mac地址
def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


# 当服务端发来消息时触发
def on_message(ws, message):
    def init():
        global client_id
        # print(message["client_id"])
        # 把服务端返回的终端ID存在全局变量中 TODO 说不定有用。。。
        client_id = message["client_id"]
        print("### Connect successfully ###")
        pass

    def send():
        print("### Send successfully ###")
        pass

    # try except 判断返回是否json传
    try:
        # JSON串转字典
        message = json.loads(message)
        # print(message)
        # 构造字典 等同switch case
        switcher = {
            "init": init,
            "send": send,
        }

        # 在字典中获取对应的方法名
        func = switcher.get(message["type"])
        # 执行方法
        func()
    except Exception as e:
        # 不是JSON串，直接打印
        print(message)
        pass
    pass


# 当发生错误时触发
def on_error(ws, error):
    print(error)
    # print(threading.enumerate())
    # print(threading.activeCount())
    pass


# 当断开连接时触发
def on_close(ws):
    print("### Connection Closed ###")
    ws_reopen()
    pass


# 当连接成功时触发
def on_open(ws):
    # 开启一个线程 调用run方法
    try:
        send_thread = threading.Thread(target=run, args=(ws,), name="send_thread")
        send_thread.start()
        global thread_list
        thread_list.append(send_thread)
    except Exception as e:
        print(e)
        pass
    pass


# 签名方法 TODO
# 目前是对应DS中functions里面的securityPwd方法
# SECURITY_KEY是DS中的常量，必须与系统中一致
def sign():
    SECURITY_KEY = "4329098asdkae"
    md5_obj = hashlib.md5(mac.encode("utf8"))
    mac_md5 = md5_obj.hexdigest()
    md5_obj = hashlib.md5(mac_md5.encode("utf8"))
    md5_obj.update("salt".encode("utf8"))
    md5_obj.update(SECURITY_KEY.encode("utf8"))
    return md5_obj.hexdigest()
    pass


# 线程运行方法
def run(*args):
    # print(args)
    ws = args[0]
    # 要发送的信息列表
    data = {
        'mac': mac,
        'sign': sign()
    }
    # 列表转JSON
    json_data = json.dumps(data)
    while (1):
        global thread_list
        for index, thread in enumerate(thread_list):
            try:
                thread_state_list[index] = thread.isAlive()
                pass
            except Exception as e:
                thread_state_list.append(thread.isAlive())
                pass
            pass
        print(thread_list)
        print(thread_state_list)
        print(threading.activeCount())
        # 往服务端发送信息
        try:
            ws.send(json_data)
            # 休眠5秒，不计算失败情况下，等于5秒发送一次
            time.sleep(5)
        except Exception as e:
            print(e)
            break
        pass
    pass
    print("### exit while ###")
    # 主动断开websocket连接
    ws.close()
    pass


# 打开websocket连接
def ws_open():
    # 新建websocket连接
    ws = websocket.WebSocketApp(
        # websocket地址
        host,
        # 追加header
        header=["x-token:ajKfZgQAf6vIddwC",
                "x-tenant:T001124",
                "x-server:1026"],
        # 打开websocket后的回调def
        on_open=on_open,
        # 收到消息时回调
        on_message=on_message,
        # 发生错误时回调
        on_error=on_error,
        # 断开连接时回调
        on_close=on_close
    )
    # 运行WebSocket框架的事件循环 长连接
    ws.run_forever(ping_interval=10, ping_timeout=5)

    # ws.run_forever()
    pass


# 重新打开websocket连接
def ws_reopen():
    print("### Waiting for %d seconds to reconnect ###" % reconnect_wait)
    time.sleep(reconnect_wait)
    try:
        # 重新连接websocket
        ws_open()
        pass
    except Exception as e:
        print(e)
        pass
    pass


if __name__ == "__main__":
    # TODO 根据系统类型调取配置文件
    # if (sys.platform == 'win32'):
    #     pass
    # else:
    #     pass

    # 启用跟踪 开启后会打印 所有 请求相关信息
    # websocket.enableTrace(True)
    # 判断是否存在第二参数，没有就调用写死的地址
    if len(sys.argv) < 2:
        host = "ws://192.168.1.135:7272/"
    else:
        host = sys.argv[1]

    # 设备网卡MAC地址
    mac = get_mac_address()
    ws_open()
    pass
