# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 11:52
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : CacheUtils.py
# @Software: PyCharm
import json
from django.conf import settings
from django.core.cache import cache
# read cache
def read_from_cache(key):
    value = cache.get(key)
    return value

# write cache
def write_to_cache(key, value):
    cache.set(key, value, settings.DAY_REDIS_TIMEOUT)

def checkKey(key):
    return cache.has_key(key)

def deleteKey(key):
    cache.delete(key)