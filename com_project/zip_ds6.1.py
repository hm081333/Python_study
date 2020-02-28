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
    print("正在检查DS6.1版本...")
    command = 'svn update ' + ds6_1_path
    result = Cmd(command).result()
    # code=0为执行成功，其他为执行错误

    if not result['err']:

        # 本次更新版本号
        new_version = result['msg'].split(' ')[-1].strip().strip('.')
        print("版本号：" + new_version)
        # 上次更新版本号
        old_version = 0

        # 上次SVN更新版本文件
        ds6_1_version_path = ds6_1_path + os.sep + 'version'
        try:
            with open(ds6_1_version_path, 'r') as f:
                old_version = f.read()
                pass
            pass
        except Exception as e:
            print("读取上次SVN版本号失败")
            # print(e)
            pass
        pass
        if new_version == old_version and False:
            print("无需重新打包")
            exit_program(0)
            pass
        else:
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

            print("正在记录本次更新版本号")
            try:
                with open(ds6_1_version_path, 'w') as f:
                    f.write(new_version)
                    pass
                pass
            except Exception as e:
                print("记录本次更新版本号失败")
                exit_program(5)
                # print(e)
                pass
            pass
            print("记录本次更新版本号完成")
            exit_program(0)
            pass

        pass

    else:
        print("Command Execute Error")
        print("Command:" + command)
        print("Code:" + str(result['ret']))
        print("Result:" + result['res'])
        print("Error:" + result['err'])
        exit_program(1)
        pass
