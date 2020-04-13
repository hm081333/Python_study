#!/usr/bin/env python
# Encoding: UTF-8
# 打包项目的工具
import os
import sys
from tool import Args, Zip, Cmd

save_dir_path = ""
project_name = ""


def backup_database():
    print("正在备份数据库")
    command = "%s -h%s -u%s -p%s %s --default_character-set=%s > %s.sql" % (
        args_tool.get_args('mysqldump_path'),
        args_tool.get_args('db_host'),
        args_tool.get_args('db_user'),
        args_tool.get_args('db_pwd'),
        (project_name if args_tool.get_args('db_name') is None else args_tool.get_args('db_name')),
        args_tool.get_args('db_charset'),
        (save_dir_path + os.sep + project_name)
    )
    result = Cmd(
        command
    ).result()
    if result['err']:
        print("Command Execute Error")
        print("Command:" + command)
        print("Code:" + str(result['ret']))
        print("Result:" + result['res'])
        print("Error:" + result['err'])
        print("数据库备份失败，请自行备份数据库")
        # raise Exception("数据库备份失败")
        pass
    else:
        print("数据库备份成功")
        pass
    pass


if __name__ == "__main__":

    args_tool = Args(
        prog='项目打包工具',
        description='金博项目打包上测试专用',
    ).add_param(
        "-h",
        "--help",
        action="help",
        help="显示帮助信息并退出"
    ).add_param(
        "-v",
        "--version",
        # 操作类型，版本号，打印后会自动退出程序
        action="version",
        # 打印的信息
        version="%(prog)s" + "\tv" + '1.0.0' + "\t构建于\t" + '2019/07/30',
        help="显示打包工具版本"
    ).add_param(
        "-pp",
        "--project-path",
        dest="project_path",
        metavar="路径",
        help="项目目录 必填"
    ).add_param(
        "-zp",
        "--zip-path",
        dest="zip_path",
        metavar="路径",
        help="打包保存目录 默认存放在项目同级目录"
    ).add_param(
        "-mp",
        "--mysqldump-path",
        dest="mysqldump_path",
        default="mysqldump",
        metavar="可执行文件路径",
        help="转存储数据库程序路径，一般位于mysql目录下bin目录里 默认值：mysqldump"
    ).add_param(
        "-ip",
        "--ignore-path",
        dest="ignore_path",
        default=".svn,.idea,runtime",
        metavar="目录名",
        help="项目打包忽略目录，多目录“,”分隔 默认值：.svn,.idea,runtime"
    ).add_param(
        "-dbh",
        "--db-host",
        dest="db_host",
        default="192.168.1.200",
        metavar="数据库IP",
        help="项目数据库IP 默认值：192.168.1.200"
    ).add_param(
        "-dbu",
        "--db-user",
        dest="db_user",
        default="root",
        metavar="数据库账号",
        help="项目数据库账号 默认值：root"
    ).add_param(
        "-dbp",
        "--db-pwd",
        dest="db_pwd",
        default="windows",
        metavar="数据库密码",
        help="项目数据库密码 默认值：windows"
    ).add_param(
        "-dbn",
        "--db-name",
        dest="db_name",
        default=None,
        metavar="数据库名称",
        help="项目数据库名称 默认值：打包目录文件夹名称"
    ).add_param(
        "-dbc",
        "--db-charset",
        dest="db_charset",
        default="utf8",
        metavar="数据库编码",
        help="项目数据库编码 默认值：utf8"
    )

    # 传入参数不足
    if args_tool.get_args('project_path') is None:
        print("缺少项目路径参数")
        sys.exit(1)
        pass

    ignore_path = args_tool.get_args('ignore_path')

    # 待打包项目路径
    project_file_path = os.path.normpath(args_tool.get_args('project_path'))
    # 路径为空
    if len(project_file_path) == 0:
        print("缺少项目路径参数")
        sys.exit(1)
        pass
    # 判断待链接文件是否存在
    elif not os.path.exists(project_file_path):
        print("项目路径不存在")
        sys.exit(2)
        pass
    # 判断传入参数是文件还是目录
    elif not os.path.isdir(project_file_path):
        print("参数不是一个项目路径")
        sys.exit(3)
        pass

    # 拆解路径
    project_file_path_arr = os.path.split(os.path.normpath(project_file_path))
    # 上级目录
    parent_file_path = project_file_path_arr[0]
    # 项目目录名
    project_name = project_file_path_arr[1]

    if args_tool.get_args('zip_path') is not None:
        # 传入 打包文件存放目录路径
        save_dir_path = os.path.normpath(args_tool.get_args('zip_path'))
        pass
    else:
        # 没有传入打包文件存放目录路径
        # 存放到上级目录
        save_dir_path = parent_file_path
        pass

    try:
        # 备份数据库
        # backup_database()
        # 执行压缩方法
        print("正在打包压缩代码文件")
        Zip(
            # 待压缩目录
            zip_path=project_file_path,
            # 压缩文件位置
            zip_file=save_dir_path + os.sep + project_name + '.zip',
            # 保留一级目录
            keep_primary_dir=True,
            # 忽略压缩目录 相对路径
            ignore_path=ignore_path,
        )
        print("打包压缩成功")
        pass
    except Exception as e:
        print(e)
        print("项目打包失败")
        sys.exit(5)
        pass
