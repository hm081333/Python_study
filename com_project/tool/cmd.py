class Cmd(object):
    from subprocess import Popen, PIPE

    command = None

    def __init__(self,
                 # 执行的命令
                 cmd=None,
                 ):  # 类似构造函数

        if cmd is None:
            raise Exception("需要传入待执行命令")
            pass
        # 创建一个解析对象
        self.command = self.Popen(
            cmd,
            stdin=self.PIPE,
            stdout=self.PIPE,
            stderr=self.PIPE,
            shell=True)
        pass

    def result(self):
        ret = self.command.wait()
        out, err = self.command.communicate()
        from chardet import detect
        # 命令行编码
        encoding = detect(out)['encoding'] if detect(out)['encoding'] is not None else detect(err)['encoding']
        # windows 的命令行默认为GBK编码
        encoding = 'gbk' if encoding is None else encoding

        return {
            'ret': ret,
            'res': out.decode(encoding),
            'err': err.decode(encoding),
        }
        pass

    pass
