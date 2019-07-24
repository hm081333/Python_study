#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import threading
# import json

try:
    # 尝试引入requests库
    import requests
except ImportError:
    # 引入失败
    try:
        # 执行安装requests库命令
        os.system("pip install requests || easy_install requests")
        pass
    except OSError:
        # 安装失败
        print("Unable to install requests library! Exit!")
        # 退出
        sys.exit(1)
        pass
    import requests
    pass


""" 常量 """
root_path = ""
eth_api = "https://api.etherscan.io"
address_constant = ""


def transactions(transactions_item):
    if 'creates' in transactions_item or not transactions_item['to']:
        return False
    if address_constant.lower() == transactions_item['to'].lower():
        pass
    pass


if __name__ == "__main__":
    num = 6295176
    tag = hex(num)
    try:
        res = requests.get(
            eth_api+"/api?module=proxy&action=eth_getBlockByNumber&tag="+tag+"&boolean=true")
        result_json = res.json()
        # result_json={'jsonrpc': '2.0', 'id': 1, 'result': None}
        if 'result' in result_json and isinstance(result_json['result'], (dict)):
            result = result_json['result']
            # print('transactions' in result)
            # print(type(result['transactions']))
            # print(isinstance(result['transactions'], (list)))
            if 'transactions' in result and isinstance(result['transactions'], (list)):
                transactions_list = result_json['result']['transactions']
                # print(transactions_list)
                for transactions_item in transactions_list:
                    transactions(transactions_item)
                    pass
                pass
            pass
        pass
    except Exception as e:
        print('ETH抓取数据失败 --- ' + str(num) + ' --- ' + str(e))
        pass

    # result=json.dumps(result_json)

    sys.exit(0)

    pass
