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
		self.length = 0
	
	def run(self):
		# run([form, parse, save] check)
		num = 0
		for html in self.htmls:
			num += 1
			print(" >>> 进行第 {} / {} 个文档处理 >>>".format(num, len(self.htmls)))
			error_msg, warn_msg, response = self.form(html)
			if DEBUGTOGGLE:
				print("[{}]{}: {}".format(now(), 'error_msg', error_msg))
				print("[{}]{}: {}".format(now(), 'warn_msg', warn_msg))
				print("[{}]{}: {}".format(now(), 'response', response))
			# 调试信息
			# print("调试信息：", response)
			if warn_msg:
				print(warn_msg)
			if error_msg:
				print(' ! 发现错误，中断进程！错误原因：' + error_msg)
				continue
			source_list, tableDict = self.parse(html, response)
			if DEBUGTOGGLE:
				print("[{}]{}: {}".format(now(), 'source_list', source_list))
				print("[{}]{}: {}".format(now(), 'tableDict', tableDict))
			result_msg = self.save(source_list, tableDict)
			print(result_msg)
		# self.check()
	
	def form(self, html):
		# run -> form
		warn_msg = ""
		doc = pq(html)
		title = returnDoc(doc, 'ul.menuList li.selected .selected-mask+a.nameWrapper span.name').strip()
		formList = FORMDIC.get(title, {})
		error_msg = ''
		response = {"title": title}
		if (len(html) != 0) and (len(html) == self.length):
			warn_msg = " @ 本条记录可能因为网页未刷新重复录入，请检查！--- @@@ --- @@@ ---"
		self.length = len(html)
		for key, value in formList.items():
			parseContent = returnDoc(doc=doc, text=value['text'], mode=value.get('mode', ''), arg=value.get('arg',''))
			response.update({key: parseContent})
			# Ver_0.4.0 length
			if value.get('mode', '') == "length":
				if parseContent > value['length']:
					error_msg += '【' + value["alias"] + '】 选择过多，不符合录入规范！ '
				else:
					continue
			if (value.get("content", "") != "return") and (parseContent != value['content']):
				# Ver_0.2.3 condition
				if value.get("condition"):
					if response.get(value["condition"][0]) == value["condition"][1]:
						error_msg += '【' + value["alias"] + '】 界面选择有误！ '
				else:
					error_msg += '【' + value["alias"] + '】 界面选择有误！ '
		return error_msg, warn_msg, response
	
	def parse(self, html, response):
		# run -> parse
		doc = pq(html)
		source_list = []
		if response["title"] == "市场大盘":
			selector = response["title"]
			title_1 = ["category", "trade_index", "trade_growth", "payment_amount_of_parent", "orders_paid_of_parent"]
			title_2 = ["category", "sales", "sales_of_parent", "saled_sales", "saled_sales_of_parent"]
			data = self.processor(doc=doc, text='#cateCons .ant-table-tbody', data={}, title=title_1)
			data = self.processor(doc=doc, text='#cateOverview .ant-table-tbody', data=data, title=title_2)
			source_list = []
		elif response["title"] == "市场排行":
			selector = response["rankname"] + response["ranktype"]
			title = RANKDIC[selector]["title"]
			if response["rankname"] == "店铺":
				eq = 1
				key_name_text = 'div.sycm-common-shop-td'
			elif response["rankname"] == "商品":
				eq = 0
				key_name_text = 'div.sycm-goods-td'
			elif response["rankname"] == "品牌":
				eq = 0
				key_name_text = 'div.sycm-common-shop-td'
			data = self.processor(doc=doc, text='.ant-table-tbody', data={}, title=title, eq=eq, key_name_text=key_name_text)
			source_list = []
		elif response["title"] == "搜索排行":
			selector = response["rankname"] + response["ranktype"]
			title = RANKDIC[selector]["title"]
			eq = 0
			key_name_text = 'span.indent-level-0'
			data = self.processor(doc=doc, text='.ant-table-tbody', data={}, title=title, eq=eq,
			                      key_name_text=key_name_text, p=True)
			source_list = []
		elif response["title"] == "属性洞察":
			selector = response["ranktype"] + response["root"].split(">")[-1].strip() + response["type"]
			title = RANKDIC[selector]["title"]
			eq = 0
			if response["ranktype"] == "店铺":
				eq = 0
				key_name_text = 'div.sycm-common-shop-td'
			elif response["ranktype"] == "商品":
				eq = 0
				key_name_text = 'div.sycm-goods-td'
			data = self.processor(doc=doc, text='.ant-table-tbody', data={}, title=title, eq=eq,
				                      key_name_text=key_name_text, p=True, page=int(response["page"]))
			source_list = []
		# 将 title 中的第一项回复到列表中
		for key, value in data.items():
			data[key].update({RANKDIC[selector]["title"][0]: key})
			source_list.append(value)
		# 处理列表中的 response ，加入到待存入 mysql 列表中：
		for updateTitle in UPDATEDIC[response["title"]]:
			# print('____________updateTitle: ', updateTitle)
			if response.get(updateTitle, ""):
				for index in range(len(source_list)):
					source_list[index].update({updateTitle: response[updateTitle]})
		return source_list, RANKDIC[selector]
			
	def processor(self, doc, text='', data={}, title=[], eq=0, key_name_text='div.sycm-common-shop-td', p=False, page=0):
		docs = doc(text).eq(eq)
		rankPlus = 1
		for item in docs('tr').items():
			location = 0
			for td in item('td').items():
				if p:
					for key in td(key_name_text).parent().items():
						key_name = key.text().replace("较前一日", "").split('\n')[0].strip()
						# 针对关键词可能出现的..情况
						if key_name[-2:] == "..":
							for i in key('span').items():
								if i.attr('title'):
									key_name = i.attr("title")
						if data.get(key_name, "") == "":
							data[key_name] = {}
						if page != 0:
							data[key_name]["rank"] = str((page - 1) * 100 + rankPlus)
							rankPlus += 1
				else:
					for key in td(key_name_text).items():
						key_name = key.text().replace("较前一日", "").split('\n')[0].strip()
						if data.get(key_name, "") == "":
							data[key_name] = {}
				for value in td('div span.alife-dt-card-common-table-sortable-value').items():
					source = value.text()
					if source == "-":
						source = "0"
					if ">99999%" in source:
						source = "9999.99"
					if "," in source:
						source = source.replace(",", "")
					if "%" in source:
						source = '%.4f' % (float(source[:-1]) / 100)
					data[key_name].update({title[location]: source})
				# 补充内容
				try:
					img = str(td('img').attr("src")).split(".jpg")[0] + ".jpg"
					if img != "None.jpg":
						data[key_name]["img"] = img[:100]
				finally:
					pass
				try:
					shop_name = td('p.goodsShopName').text()
					if shop_name:
						data[key_name]["shop_name"] = shop_name
				finally:
					pass
				try:
					item_id_list = str(td('a').attr('href')).split("?id=")
					if len(item_id_list) > 1:
						data[key_name]["item_id"] = item_id_list[1]
				finally:
					pass
				# 顺序迭代
					location += 1
		return data
	
	def processor_notitle(self, doc, text='', data={}, titile=[], key_name_text=''):
		pass
	
	def save(self, source_list, tableDic):
		# run -> save
		# print(source_list)
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

