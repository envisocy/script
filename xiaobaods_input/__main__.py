#!usr/bin/env python
# -*- coding:utf-8 -*-

import commandLine
import document
import bsparse

# 命令行模式
# Exp: python xiaobaods_input arguments

def getArgv():
	try:
		import sys
		argv = sys.argv[1:]
	except:
		argv = []
	return argv


if __name__ == '__main__':
    argv = getArgv()
    # 实例化命令行模块
    cl = commandLine.COMMANDLINE(argv)
    # 显示传入的参数
    type, length = cl.log()
    method, argument = cl.parseCommandLine()
    # 进行数据输出
    doc = document.Doc()
    data = doc.getData()
    # bs: data = [html, html, ...]
    if method == 'bs':
	    pb = bsparse.ParseBS(data)
	    pb.run()
    
    