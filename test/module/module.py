#!/usr/bin/env python
# Encoding: UTF-8

class GetMac(object):
    mac = ""

    def __init__(self,
                 upper=False,
                 lower=False,
                 colon=False
                 ):  # 类似构造函数
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int=node).hex[-12:]
        if (upper):
            mac = mac.upper()
            pass
        elif lower:
            mac = mac.lower()
            pass

        if colon:
            old_mac = mac
            mac = ""
            for index, char in enumerate(old_mac):
                mac += char
                if index % 2:
                    mac += ":"
                    pass
                pass
            mac = mac[0:-1]
            pass
        else:
            mac = mac.replace(":", "")
            pass

        self.mac = mac
        pass

    pass


class Json(object):
    import json as json_module
    debug = False

    def __init__(self, debug=False):  # 类似构造函数
        self.debug = debug
        pass

    def load(self, json_str):
        return self.json_module.loads(json_str)
        pass

    def file_load(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return self.json_module.load(f)
                pass
            pass
        except Exception as e:
            print("fail to read file")
            print(e)
            pass
        pass

    def dump(self, obj):
        return self.json_module.dumps(obj)
        pass

    def file_dump(self, file_path, obj):
        try:
            with open(file_path, 'w') as f:
                self.json_module.dump(obj, f)
                pass
            pass
        except Exception as e:
            print("fail to write file")
            print(e)
            pass
        pass

    pass
