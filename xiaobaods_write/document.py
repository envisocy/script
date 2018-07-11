# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

import os
import re
from pyquery import PyQuery as pq

from xiaobaods_write.config import *

class Doc():
	def __init__(self, filename=FILENAME):
		try:
			with open(DESKTOP_DIR + os.sep + filename, 'r', encoding="gb18030") as f:
				html = f.read()
		except:
			with open(DESKTOP_DIR + os.sep + filename, 'r', encoding="utf8") as f:
				html = f.read()
		pattern = re.compile('(<html.*?</html>)', re.S)
		htmls = re.findall(pattern, html)
		self.msg = " *** 载入文档并初始化信息 ***\n * From: {}{}{}\n * Details: {} bytes ( {} Blocks )\n ***" \
		           " *** *** *** *** *** ***\n".format(DESKTOP_DIR, os.sep, filename, len(html), len(htmls))
		self.htmls = htmls

	def run(self):
		for html in self.htmls:
			self.parse(html)
			self.msg += " * {}".format(self.mode)
	
	def parse(self, html):
		doc = pq(html)
		if doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "品牌粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
			# 商品店铺榜 - 品牌粒度
			self.mode = "品牌粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "行业粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
			# 商品店铺榜 - 行业粒度
			self.mode = "行业粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "属性粒度" and doc(".active.ui-tab-head-item").text() == "热销商品榜":
			# 商品店铺榜 - 属性粒度
			self.mode = "属性粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".breadcrumb .active").text() == "商品详情":
			# 商品店铺榜 - 商品详情（商品详细数据）
			self.mode = "商品详情"
