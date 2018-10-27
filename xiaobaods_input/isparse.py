# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/10/27 16:05'

from pyquery import PyQuery as pq
import pandas as pd
import os

from setting import FILEDIR

class ParseIS():
	def __init__(self, htmls):
		self.htmls = htmls
		self.length = 0
		self.filename = "InSaleList.xls"

	def run(self):
		num = 0
		source_list = []
		for html in self.htmls:
			num += 1
			print(" >>> 进行第 {} / {} 个文档处理 >>>".format(num, len(self.htmls)))
			source_list = self.parse(html, source_list)
		result_msg = self.save(source_list)
		print(result_msg)

	def parse(self, html, source_list):
		doc=pq(html)
		if doc(".tree-select-content").html() == "请选择":
			batch = "all"
		else:
			batch = doc(".tree-select-content").html()
		for item in doc(".sui-table-tbody  .sui-table-row").items():
			source_list.append({
				"batch": batch,
				"style_coding": item(".goods-item-outerid span:nth-child(2)").text(),
				"spuid": item(".goods-item-id").text().split("：")[1],
			})
		return source_list
	
	def save(self, source_list):
		df = pd.DataFrame(source_list)
		df.to_excel(FILEDIR + os.sep + self.filename, index=False)
		return " * " + FILEDIR + os.sep + self.filename + " Completed Created!"