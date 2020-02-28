#!/usr/bin/env python
# Encoding: UTF-8
# 把项目yaconf配置文件创建链接到yaconf配置目录
import os
import sys
from tool import Args, Cmd

# del "D:\phpStudy\yaconf\190316sz_yz_app.ini"
# mklink "D:\phpStudy\yaconf\190316sz_yz_app.ini" "E:\WWW\19-03\190316szyz_ds\190316sz_yz_app.ini"
# E:\WWW\link_yaconf_ini.exe E:\WWW\19-03\190316szyz_ds\190316sz_yz_app.ini
# D:\phpStudy\php\php-7.3-nts-x64\php.exe

if __name__ == '__main__':
    args_tool = Args(
        prog='项目配置迁移工具',
        description='金博项目配置文件链接到Yaconf目录',
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
        version="%(prog)s" + "\tv" + '1.0.0' + "\t构建于\t" + '2019/07/31',
        help="显示配置工具版本"
    ).add_param(
        "-cf",
        "--config-file",
        dest="config_file",
        metavar="配置文件路径",
        help="配置文件路径 必填"
    ).add_param(
        "-pe",
        "--php-exec",
        dest="php_exec",
        default="php",
        metavar="配置文件路径",
        help="配置文件路径 必填"
    )

    # PHP路径
    php_exec = os.path.normpath(args_tool.get_args('php_exec'))
    if not os.path.isfile(php_exec):
        print("PHP程序路径错误")
        sys.exit(1)
        pass

    # 待链接的配置文件路径
    conf_file_path = args_tool.get_args('config_file')
    # 路径为空
    if len(conf_file_path) == 0:
        print("缺少配置文件参数")
        sys.exit(2)
        pass
    # 判断待链接文件是否存在
    elif not os.path.exists(conf_file_path):
        print("配置文件不存在")
        sys.exit(3)
        pass
    # 判断传入参数是文件还是目录
    elif not os.path.isfile(conf_file_path):
        print("传入路径不是一个文件")
        sys.exit(4)
        pass

    # 获取文件名
    conf_file_name = os.path.basename(conf_file_path)
    # 文件名拆解
    file_pathinfo = os.path.splitext(conf_file_name)
    # 项目名
    project_name = file_pathinfo[0]
    # 文件扩展名
    file_extension = file_pathinfo[1]
    # 文件类型不是ini
    if file_extension != '.ini':
        print("文件类型错误")
        sys.exit(5)
        pass

    # php -r "echo ini_get('yaconf.directory');"
    # php获取yaconf配置目录的语句
    get_yaconf_dir_cmd = php_exec + ' -r "echo ini_get(\'yaconf.directory\');"'
    # 命令行运行结果
    get_yaconf_dir_res = Cmd(get_yaconf_dir_cmd).result()

    # code=0为执行成功，其他为执行错误
    if get_yaconf_dir_res['err']:
        print("Command Execute Error")
        print("Command:" + get_yaconf_dir_cmd)
        print("Code:" + str(get_yaconf_dir_res['ret']))
        print("Result:" + get_yaconf_dir_res['res'])
        print("Error:" + get_yaconf_dir_res['err'])
        print("Exit")
        sys.exit(6)
        pass

    # 配置的目录
    yaconf_dir_path = get_yaconf_dir_res['res']
    # 是否存在目录
    if not os.path.isdir(yaconf_dir_path):
        print("Yaconf配置目录不存在")
        sys.exit(7)
        pass

    # 获取路径（去除路径path中的冗余）
    yaconf_dir_path = os.path.normpath(yaconf_dir_path)
    # 配置保存到Yaconf目录下的路径
    conf_yaconf_file_path = yaconf_dir_path + os.sep + conf_file_name
    # 为文件dst创建软链接，src为软链接文件的路径。相当于$ln -s命令。
    # result = os.symlink(conf_file_path, conf_yaconf_file_path)

    # Yaconf目录 是否已经存在该配置文件
    if os.path.isfile(conf_yaconf_file_path):
        # 删除Yaconf目录中存在的原文件
        del_conf_cmd = 'del ' + conf_yaconf_file_path
        # 命令行运行结果
        del_conf_res = Cmd(del_conf_cmd).result()
        # 结束代码不是0 - 操作失败
        if del_conf_res['err']:
            print("Command Execute Error")
            print("Command:" + del_conf_cmd)
            print("Code:" + str(del_conf_res['ret']))
            print("Result:" + del_conf_res['res'])
            print("Error:" + del_conf_res['err'])
            print("Exit")
            sys.exit(8)
            pass
        pass

    mklink_conf_cmd = 'mklink ' + conf_yaconf_file_path + ' ' + conf_file_path
    mklink_conf_res = Cmd(mklink_conf_cmd).result()
    if mklink_conf_res['err']:
        print("Command Execute Error")
        print("Command:" + mklink_conf_cmd)
        print("Code:" + str(mklink_conf_res['ret']))
        print("Result:" + mklink_conf_res['res'])
        print("Error:" + mklink_conf_res['err'])
        print("Exit")
        sys.exit(9)
        pass

    print("迁移成功")
    pass
