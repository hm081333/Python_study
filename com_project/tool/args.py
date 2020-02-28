class Args(object):
    import argparse
    parser = None

    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - prog -- 应用程序名称 (默认: sys.argv[0])
        - description -- 该程序的功能描述
        - epilog -- 参数描述后面的文字
        - add_help -- 添加帮助选项
    """

    def __init__(self,
                 prog="应用程序名称",
                 description="应用程序描述",
                 epilog="更多问题请咨询开发者。",
                 add_help=False,
                 ):  # 类似构造函数
        # 创建一个解析对象
        self.parser = self.argparse.ArgumentParser(
            # 程序名
            prog=prog,
            # help时显示的开始文字
            description=description,
            # help时显示的结尾文字
            epilog=epilog,
            # 是否增加-h/--help选项
            add_help=add_help,
        )
        pass

    def add_param(self, *args, **kwargs):
        self.parser.add_argument(
            *args, **kwargs
        )
        return self
        pass

    # 构建传入参数解析
    def get_args(self, name=None, return_dict=False):
        # 获取传入参数 Namespace
        all_args = self.parser.parse_args()
        # 要求返回字典 或者 指定获取某参数的值
        if return_dict or name is not None:
            # 把Namespace转换为字典
            all_args_obj = vars(all_args)
            if name is not None:
                if name not in all_args_obj:
                    return None
                else:
                    return all_args_obj[name]
                pass
            return all_args_obj

        # 返回解析参数
        return all_args

    pass
