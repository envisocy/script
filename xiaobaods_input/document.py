# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/9/25 11:53'


import re

from setting import *


# 定义数据格式
class Doc():
	def __init__(self, method='bs', log=False):
		# 通过 self.htmls 也可以获得具体的信息
		# 执行数据处理的方式
		self.method = method
		# 预留的显示参数
		self.log = log
		self.parseData()
	
	def parseData(self):
		# 数据获取方式，并进行找寻文件，读取文件操作
		if self.method == 'bs':
			try:
				with open(FILEDIR + os.sep + FILENAME, 'r', encoding="gb18030") as f:
					html = f.read()
			except:
				with open(FILEDIR + os.sep + FILENAME, 'r', encoding="utf8") as f:
					html = f.read()
			pattern = re.compile('(<html.*?</html>)', re.S)
			htmls = re.findall(pattern, html)
			self.msg = " * From: {}\{}\n * Details: {} bytes ( {} Blocks )".format(FILEDIR,
			                                                                       FILENAME, len(html), len(htmls))
			self.htmls =  htmls
	
	def getData(self):
		# 出口函数：打印信息，并返回处理后的数据
		print(" *** 生意参谋商品信息模块 ***\n" + self.msg + "\n * A new processing engine: Ailurus fulgens X" +
		                                           "\n *** *** *** *** *** *** ***")
		return self.htmls