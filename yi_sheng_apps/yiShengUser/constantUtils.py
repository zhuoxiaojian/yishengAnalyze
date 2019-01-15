# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 11:57
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : constantUtils.py
# @Software: PyCharm
class ConstantUtil:

    #校验手机号正则
    REGEX_MOBILE = "^(13[0-9]{9})|(18[0-9]{9})|(14[0-9]{9})|(17[0-9]{9})|(15[0-9]{9})|((19[8|9])\d{8})$"

    #验证码类型
    LOGIN_CODE_TYPE = 'LOGIN'
    REGISTRY_CODE_TYPE = 'REGISTRY'

    #缓存用户信息过期时间
    LOGIN_INFO_EXPIRE = 30*60

    #图片验证码缓存时间
    VERIFY_CODE_EXPIRE = 2*60

    TOKEN_KEY_PRE = 'TOKEN'

    #易数宝应用
    APP_YSB = 'YSB'
    YSB_REGISTRY = '0'
    YSB_LOGIN = '1'

    #汇桔宝应用
    APP_HJB = 'HJB'
    HJB_REGISTRY = '0'
    HJB_LOGIN = '1'