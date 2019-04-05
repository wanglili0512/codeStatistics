import hashlib

from settings import Config


def md5(pwd):
    """
    将密码加密
    :param pwd: 要加密的密码
    :return: 加密后的结果
    """
    obj = hashlib.md5(Config.SALT)
    obj.update(pwd.encode('utf-8'))
    v = obj.hexdigest()
    return v
