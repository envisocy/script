# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/9/25 11:53'

from pyquery import PyQuery as pq
import pymysql

import configure

from setting import *

class ParseBS():
	def __init__(self, htmls):
		self.htmls = htmls
	
	def run(self):
		# run([form, parse, save] check)
		num = 0
		for html in self.htmls:
			num += 1
			print(" >>> 进行第 {} 个文档处理 >>>".format(num))
			error_msg, response = self.form(html)
			# print(response)
			if error_msg != '':
				print(' ! 发现错误，中断进程！错误原因：' + error_msg)
				continue
			source_list, tableDict = self.parse(html, response)
			result_msg = self.save(source_list, tableDict)
			print(result_msg)
		# self.check()
	
	def form(self, html):
		# run -> form
		doc = pq(html)
		title = returnDoc(doc, 'ul.menuList li.selected .selected-mask+a.nameWrapper span.name').strip()
		formList = FORMDIC.get(title, {})
		error_msg = ''
		response = {"title": title}
		for key, value in formList.items():
			parseContent = returnDoc(doc=doc, text=value['text'], mode=value.get('mode', ''), arg=value.get('arg',''))
			response.update({key: parseContent})
			if (value.get("content", "") != "return") and (parseContent != value['content']):
				error_msg += '【' + value["alias"] + '】 界面选择有误！ \t'
		return error_msg, response
	
	def parse(self, html, response):
		# run -> parse
		doc = pq(html)
		source_list = []
		if response["title"] == "市场大盘":
			title_1 = ["category", "trade_index", "trade_growth", "payment_amount_of_parent", "orders_paid_of_parent"]
			title_2 = ["category", "sales", "sales_of_parent", "saled_sales", "saled_sales_of_parent"]
			data = self.market_quotations(doc=doc, text='#cateCons .ant-table-tbody tr', data={}, title=title_1)
			data = self.market_quotations(doc=doc, text='#cateOverview .ant-table-tbody tr', data=data, title=title_2)
			source_list = []
			for key, value in data.items():
				data[key].update({'category': key})
				source_list.append(value)
			for updateTitle in UPDATEDIC[response["title"]]:
				# print('____________updateTitle: ', updateTitle)
				if response.get(updateTitle, ""):
					for index in range(len(source_list)):
						source_list[index].update({updateTitle: response[updateTitle]})
		return source_list, TABLEDIC[response["title"]]
			
	def market_quotations(self, doc, text='#cateCons .ant-table-tbody tr', data={}, title=[]):
		for item in doc(text).items():
			location = 1
			for td in item('td').items():
				for key in td('div.sycm-common-shop-td').items():
					key_name = key.text().replace("较前一日", "")
					if data.get(key_name, "") == "":
						data[key_name] = {}
				for value in td('div span.alife-dt-card-common-table-sortable-value').items():
					source = value.text()
					if ">99999%" in source:
						source = "9999.99"
					if "%" in source:
						source = '%.4f' % (float(source[:-1]) / 100)
					if "," in source:
						source = source.replace(",", "")
					data[key_name].update({title[location]: source})
					location += 1
		return data
	
	def save(self, source_list, tableDic):
		# run -> save
		result_msg = ""
		for sql in SQL_LIST_PATTERN:
			sentence = ""
			for source in source_list:
				key =  str([i for i in source.keys()]).replace("'", "`").replace("[", "(").replace("]", ")")
				value =  str([i for i in source.values()]).replace("[", "(").replace("]", ")")
				sentence += "REPLACE INTO {} {} VALUES{};".format(tableDic["table"], key, value)
			result = self.call_sql(sql, sentence)
			result_msg += " * {}: {}\n".format(sql, result)
		return result_msg[:-2]

	def call_sql(self, sql, sentence):
		# print("sentence: ", sentence)
		conn = pymysql.connect(
			host=configure.echo(sql)["config"]["host"],
			port=configure.echo(sql)["config"]["port"],
			user=configure.echo(sql)["config"]["user"],
			passwd=configure.echo(sql)["config"]["passwd"],
			charset=configure.echo(sql)["config"]["charset"],
			db="baoersqlbs")
		try:
			cursor = conn.cursor()
			cursor.execute(sentence)
			conn.commit()
			data = cursor.fetchall()
		finally:
			cursor.close()
			conn.close()
		if data:
			result = [i[0] for i in data]
		else:
			result = "Completed Saved!"
		return result

