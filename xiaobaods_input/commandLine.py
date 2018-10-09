#!usr/bin/env python
# -*- coding:utf-8 -*-

import re

from setting import DEBUGTOGGLE


class COMMANDLINE():
	def __init__(self, type):
		self.args = type
		self.method = ""
		self.argument = ""
	
	def log(self):
		# 仅输出传入参数，参数全内容 及 可识别的参数的个数
		if DEBUGTOGGLE:
			print(' * 运行参数为：{} (识别参数个数: {})'.format(self.args, len(self.args)))
		return self.args, len(self.args)
	
	def parseCommandLine(self):
		# 返回被格式化后的 method 和 其他参数
		if len(self.args) == 1:
			if self.args[0] != '':
				self.method = self.args[0]
			else:
				self.method = 'bs'
			self.argument = ''
		elif len(self.args) >= 2:
			self.method = self.args[0]
			self.argument = self.args[1:len(self.args)]
			# 默认参数判断
		if DEBUGTOGGLE:
			print(' * 已处理数据： {}, {}'.format(self.method, self.argument))
		return self.method, self.argument