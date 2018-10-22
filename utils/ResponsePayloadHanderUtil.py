# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 10:20
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : ResponsePayloadHanderUtil.py
# @Software: PyCharm
def jwt_response_payload_handler(token, user=None, request=None):
    '''
    自定义jwt认证成功返回数据
    :param token:
    :param user:
    :param request:
    :return:
    '''
    return {'token': token}