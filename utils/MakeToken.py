# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 10:54
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : MakeToken.py
# @Software: PyCharm
import time
import hashlib
'''
根据用户名和时间戳生成用户登录成功的随机字符串
'''
def get_token_code(username):
    timestamp = str(time.time()) #当前时间戳
    m = hashlib.md5(bytes(username, encoding='utf8'))
    m.update(bytes(timestamp, encoding='utf8')) #update必须接收一个bytes
    return m.hexdigest()
