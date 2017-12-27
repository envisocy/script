#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
方便xiaobaods.com使用命令行模式传递参数给予返回结果
'''

argv = {}
if __name__ == '__main__':
    try:
        import sys
        argv = sys.argv[1]
        argv = eval(argv)
    except:
        argv = {}

import xiaobaods_output.function as function
basic = function.basic(**argv)
basic.run(argv.get("fun","a"))
