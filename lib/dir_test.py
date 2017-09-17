# Encoding: UTF-8
import os

from ly import zhcn


def ly_file(path, counts):
    if os.path.exists(path) == False:
        zhcn('不存在此目录：' + path)
        return
    if os.path.isfile(path):
        print '|-' + '---' * counts + ' ' + os.path.basename(path)
        pass
    elif os.path.isdir(path):
        print '|-' + '---' * counts + ' ' + path
        dept_paths = os.listdir(path)
        for dept_path in dept_paths:
            # 不推荐直接使用路径分隔符号 '\' '/' 推荐使用os.sep
            # if path.rfind(os.path.sep) == len(path) - 1:
            #     dept_path = path + dept_path
            #     pass
            # else:
            #     dept_path = path + os.path.sep + dept_path
            #     pass
            dept_path = os.path.join(path, dept_path)
            ly_file(dept_path, counts + 1)
            pass
    pass


# study_py_path = 'D:\\PY'
# print study_py_path
zhcn('请输入路径')
ly_file(raw_input(), 0)
