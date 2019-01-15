# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 15:19
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : BusinessUtils.py
# @Software: PyCharm
import re
class BusinessUtils(object):
    def urlFilter(self, domain):
        return domain.rstrip('/').lstrip('https://').lstrip('http://')
    def wwwFilter(self, domain):
        return domain.strip('www.')

if __name__ == '__main__':
    b = BusinessUtils()
    print(b.wwwFilter(b.urlFilter('https://www.baidu.com')))