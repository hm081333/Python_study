# 判断变量类型的函数
def typeof(variate=None):
    if isinstance(variate, int):
        return "int"
    elif isinstance(variate, str):
        return "str"
    elif isinstance(variate, float):
        return "float"
    elif isinstance(variate, list):
        return "list"
    elif isinstance(variate, tuple):
        return "tuple"
    elif isinstance(variate, dict):
        return "dict"
    elif isinstance(variate, set):
        return "set"
    else:
        return None
