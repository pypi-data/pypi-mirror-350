import hashlib


def md5_key_builder(*args, **kwargs):
    """
    计算 MD5 哈希值
    :param args: 位置参数，可以是任意类型
    :param kwargs: 关键字参数，可以是任意类型
    :return: 计算得到的 MD5 哈希值（十六进制字符串）
    """
    combined = ''.join(str(arg) for arg in args) + ''.join(f"{k}={v}" for k, v in kwargs.items())
    md5_hash = hashlib.md5()
    md5_hash.update(combined.encode())
    return md5_hash.hexdigest()