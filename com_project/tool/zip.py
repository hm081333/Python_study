class Zip(object):
    import os
    import zipfile

    zip = None

    def __init__(self,
                 # 待压缩目录
                 zip_path=None,
                 # 压缩文件位置
                 zip_file=None,
                 # 保留一级目录
                 keep_primary_dir=True,
                 # 忽略压缩目录 相对路径
                 ignore_path=None,
                 # 忽略压缩文件 相对路径
                 # ignore_file=None,
                 ):  # 类似构造函数

        if zip_path is None:
            raise ValueError("zip_path must be assign")
            pass
        elif not self.os.path.isdir(zip_path):
            raise ValueError("zip_path must be an exists dir")
            pass

        if zip_file is None:
            raise ValueError("zip_file must be assign")
            pass

        # 拆解路径
        zip_path_arr = self.os.path.split(self.os.path.normpath(zip_path))
        # 压缩目录 的 上级目录
        zip_path_parent_path = zip_path_arr[0]
        # 压缩目录 目录名
        zip_path_name = zip_path_arr[1]

        if keep_primary_dir:
            # 去掉目标和路径，保留一级目录
            del_path = zip_path_parent_path
            pass
        else:
            # 去掉目标和路径，不保留一级目录
            del_path = zip_path
            pass

        from tool.tool import typeof
        if ignore_path is not None and typeof(ignore_path) is 'str':
            # 逗号分隔拆分字符串
            ignore_path = ignore_path.split(",")
            pass

        # if ignore_file is not None and typeof(ignore_file) is 'str':
        #     # 逗号分隔拆分字符串
        #     ignore_file = ignore_file.split(",")
        #     pass

        self.open_zip(zip_file)

        for path, dirnames, filenames in self.os.walk(zip_path):
            # 去掉多余路径
            fpath = path.replace(del_path, '')
            # print(ignore_path)
            # print(set(fpath.split(self.os.sep)))
            # 含有忽略目录数量 - 是否忽略该路径
            if len(list(set(ignore_path).intersection(set(fpath.split(self.os.sep))))):
                continue
                pass

            # 打印压缩目录路径
            # print(fpath)

            for filename in filenames:
                # 文件绝对路径
                file_real_name = self.os.path.join(path, filename)
                # 文件相对路径
                file_replace_name = self.os.path.join(fpath, filename)

                # 含有忽略文件目录数量 - 是否忽略该路径
                # if len(list(set(ignore_file).intersection(set(file_replace_name.split(self.os.sep))))):
                #     continue
                #     pass
                self.add_file_to_zip(file_real_name, file_replace_name)
                pass
            pass
        self.close_zip()

        pass

    def open_zip(self, zip_file):
        # 创建或打开压缩文件
        self.zip = self.zipfile.ZipFile(zip_file, "w", self.zipfile.ZIP_DEFLATED)
        pass

    def add_file_to_zip(self, filename, replace_name):
        # 添加文件到压缩包
        self.zip.write(filename, replace_name)
        # 打印已添加文件
        print(replace_name)
        pass

    def close_zip(self):
        # 关闭压缩文件
        self.zip.close()
        pass

    # zip_dir("E:\\www\\19-07\\190723hzzz_qkl\\", "E:\\www\\190723hzzz_qkl.zip")

    pass
