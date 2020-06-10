#!/usr/bin/env python
# Encoding: UTF-8
import os
import sys

from tool import Zip, Cmd

# ds6.1目录
ds6_1_path = 'E:\\www\\test\\ds6.1'


def exit_program(exit_code):
    input("按下回车键退出")
    sys.exit(exit_code)
    pass


if __name__ == '__main__':
    # 压缩打包ds6.1
    print("正在打包压缩")
    try:
        # 执行压缩方法
        Zip(
            # 待压缩目录
            zip_path=ds6_1_path,
            # 压缩文件位置
            zip_file="E:\\www\\ds6.1.zip",
            # 保留一级目录
            keep_primary_dir=False,
            # 忽略压缩目录 相对路径
            ignore_path=[
                ".svn",
                ".idea",
                "runtime",
            ],
        )
        pass
    except Exception as e:
        print("打包压缩失败")
        print(e)
        exit_program(5)
        pass

    print("打包压缩完成")

    exit_program(0)
    pass
