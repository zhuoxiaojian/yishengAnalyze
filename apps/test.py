# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 15:23
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : test.py
# @Software: PyCharm

import imp
testRun = imp.load_source('testRun', 'D:\\yishengProject\\pythonTest\\com\\testRun.py')
# import testRun
if __name__=="__main__":
    print(testRun.getMethod(3, 4))