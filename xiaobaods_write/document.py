# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

# 生意参谋的数据收集

import re
from pyquery import PyQuery as pq
import configure
import pymysql

from xiaobaods_write.config import *

class Doc():
	def __init__(self, filename=FILENAME, detail=0):
		self.detail = detail
		try:
			with open(DESKTOP_DIR + os.sep + filename, 'r', encoding="gb18030") as f:
				html = f.read()
		except:
			with open(DESKTOP_DIR + os.sep + filename, 'r', encoding="utf8") as f:
				html = f.read()
		pattern = re.compile('(<html.*?</html>)', re.S)
		htmls = re.findall(pattern, html)
		self.msg = " *** 生意参谋商品信息模块 ***\n * From: {}{}{}\n * Details: {} bytes ( {} Blocks )\n" \
		           " * A new processing engine: Ailurus fulgens X\n *** *** *** *** *** *** ***\n".format(DESKTOP_DIR,
		                                                                    os.sep, filename, len(html), len(htmls))
		self.htmls = htmls
		self.brand_list = []    # 为结束品牌检查提供参考

	def run(self):
		print(self.msg)
		for html in self.htmls:
			self.parse(html)    # 二级解析
			self.prompt_message()
			if self.error:
				print("-!" * 30 + "\n" + self.error + "\n" + "-!" * 30 + "\n")
				continue
			result = self.parse_html(html)
			self.save_sql(result)
		self.check_sql()
	
	def parse(self, html):
		self.error = ""     # 初始化错误信息
		doc = pq(html)
		if doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "品牌粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
			self.mode = "品牌粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "行业粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
			self.mode = "行业粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
		) == "属性粒度" and doc(".active.ui-tab-head-item").text() == "热销商品榜":
			self.mode = "属性粒度"
		elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".breadcrumb .active").text() == "商品详情":
			self.mode = "商品详情"
		self.parse_content(doc)     # 套用解析
		if not self.info:
			self.error = " !!! 未解析出有效的数据内容，请检查源文件信息！"

	
	def parse_content(self, doc):
		if self.mode == "品牌粒度":
			self.info={
				"mask": "商品店铺榜",
				"header": "品牌粒度",
				"main": doc(".dtpicker-main-text .num").text(),
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1].split(".")[-1],
				"brand": doc(".brand-dropdown .btn.btn-dropdown").text(),
				"device": doc(".device-dropdown .btn.btn-dropdown").text(),
				"seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
				"head": doc(".active.ui-tab-head-item").text(),
				"quantity": doc(".config-selector .btn.btn-dropdown").text(),
				"curr": doc(".ui-pagination-curr").text(),
				"total": doc(".ui-pagination-total").text(),
			}
			# 超长品牌配置
			if self.info["brand"] == "CHNPLUM/...":
				self.info["brand"] = "CHNPLUM/华梅"
			elif self.info["brand"] == "SoleExample/独...":
				self.info["brand"] = "SoleExample/独例"
			elif self.info["brand"] == "SEHZNZIE...":
				self.info["brand"] = "SEHZNZIEZ/轩兹"
			self.brand_list.append(self.info["brand"])  # 为最终检查提供依据
		# elif self.mode == "商品详情":
		# 	if "tmall" in doc(".screen-header .item-panel .img-wrapper a").attr("href"): # 天猫
		# 		try:
		# 			shopname = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)(".slogo-shopname").text()
		# 			shopurl = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)(".slogo-shopname").attr("href").split(".com")[0]+".com"
		# 			brand = shopname.split("旗舰店")[0].split("专营店")[0].split("官方")[0].split("女装")[0].split("服饰")[0]
		# 		except:
		# 			shopname = "-"
		# 			shopurl = "-"
		# 			brand = "-"
		# 	elif "taobao" in doc(".screen-header .item-panel .img-wrapper a").attr("href"): # 淘宝
		# 		try:
		# 			shopname = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)("strong a").attr("title")
		# 			shopurl = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)("strong a").attr("href").split(".com")[0]+".com"
		# 			brand = shopname
		# 		except:
		# 			shopname = "-"
		# 			shopurl = "-"
		# 			brand = "-"
		# 	self.info={
		# 		"mask": "商品店铺榜",
		# 		"header": "商品详情",
		# 		"main": doc(".dtpicker-main-text .num").text().split()[0],
		# 		"img": doc(".item-panel .img-wrapper img").attr("src"),
		# 		"title": doc(".screen-header .item-panel").text().replace(" ",""),
		# 		'href': (doc(".screen-header .item-panel .img-wrapper a").attr("href").split("?")[0] + "?id=" + \
		# 				 doc(".screen-header .item-panel .img-wrapper a").attr("href").split("id=")[1])[:60],
		# 		"id": doc(".screen-header .item-panel .img-wrapper a").attr("href").split("id=")[1],
		# 		"shopname": shopname,
		# 		"shopurl": shopurl,
		# 		"brand": brand,
		# 	}
		elif self.mode == "行业粒度":
			self.info={
				"mask": "商品店铺榜",
				"header": "行业粒度",
				"main": doc(".dtpicker-main-text .num").text(),
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1].split(".")[-1],
				"device": doc(".device-dropdown .btn.btn-dropdown").text(),
				"seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
				"head": doc(".active.ui-tab-head-item").text(),
				"quantity": doc(".config-selector .btn.btn-dropdown").text(),
				"curr": doc(".ui-pagination-curr").text(),
				"total": doc(".ui-pagination-total").text(),
			}
		elif self.mode == "属性粒度":
			self.info={
				"mask": "商品店铺榜",
				"header": "属性粒度",
				"main": doc(".dtpicker-main-text .num").text(),
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1].split(".")[-1],
				"attribute": doc(".flex-content").text(),
				"device": doc(".device-dropdown .btn.btn-dropdown").text(),
				"seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
				"head": doc(".active.ui-tab-head-item").text(),
				"quantity": doc(".config-selector .btn.btn-dropdown").text(),
				"curr": doc(".ui-pagination-curr").text(),
				"total": doc(".ui-pagination-total").text()
			}
		else:
			self.info={}
		# main_split
		self.info["main"] = self.info["main"].split("（")[1].split("）")[0]
		if self.info.get('main').split("~")[0] == self.info.get('main').split("~")[1]:
			self.info["main"] = self.info.get('main').split("~")[0]
		else:
			self.error = " !!! 选择日期为范围，数据不符合规范！此数据被忽略！"
		# total
		if not self.info["total"]:
			self.error = " !!! 改页没有有效数据，页码为空，请检查！"
		else:
			self.info["total"] = self.info["total"][1]  # "共5页" 取页数数字
		# validation_message
		if self.mode in ["品牌粒度", "行业粒度"] and self.info.get("category") not in PERMIT[self.mode]:
				self.error = " !!! 类目选择错误或超出范围，请检查后再试！此数据被忽略！"
		if self.mode=="属性粒度" and self.info.get("attribute") not in PERMIT_attribute[self.info["category"]]:
			self.error = " !!! 属性选择错误或超出范围，请检查后再试！此数据被忽略！"
		if self.info.get("device", "所有终端") != "所有终端":
			self.error = " !!! 请选择数据源为“所有终端”，此数据被忽略！"
		if self.info.get("seller", "全网") != "全网":
			self.error = " !!! 请选择数据源渠道为“全网”，此数据被忽略！"
		if self.info.get("quantity", "100") != "100":
			self.error = " !!! 请选择每页最大显示数为100，并重新处理该部分数据！"
	
	def prompt_message(self):
		if self.mode == "品牌粒度":
			if self.detail == 0:
				print("- 〔", self.mode, self.info.get('head'), "〕日期：", self.info.get('brand'), "@", self.info.get('main'),
				      " Page: ", self.info.get("curr"), "/", self.info.get("total"))
			elif self.detail == 1:
				print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
				print("- 参数：〖", self.info.get('main'), "/", self.info.get('category'), "/", self.info.get('brand'),
				      "/", self.info.get('device'), "/", self.info.get('seller'), "〗")
				print("- 细节：〔", self.info.get('head'), "〕 Max items: ", self.info.get('quantity'), " Page: ",
				      self.info.get("curr"), "/", self.info.get("total"))
		# elif self.mode == 2:
		# 	if self.detail == 0:
		# 		print("- 〔", self.info.get('id'), "〕品牌：", self.info.get('brand'), " 日期：", self.info.get('main'))
		# 	elif self.detail == 1:
		# 		print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
		# 		print("- 参数：〖", self.info.get('main'), "@", self.info.get('title'), "〗")
		# 		print("- 商品ID：〔", self.info.get('id'), "〕", self.info.get('shopname'), ": ", self.info.get("brand"))
		elif self.mode == "行业粒度":
			if self.detail == 0:
				print("- 〔", self.mode, self.info.get('head'), "〕类目：", self.info.get('category'), "@", self.info.get('main'),
				      " Page: ", self.info.get("curr"), "/", self.info.get("total"))
			elif self.detail == 1:
				print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
				print("- 参数：〖", self.info.get('main'), "/", self.info.get('category'), "/", self.info.get('brand'),
				      "/", self.info.get('device'), "/", self.info.get('seller'), "〗")
				print("- 细节：〔", self.info.get('head'), "〕 Max items: ", self.info.get('quantity'), " Page: ",
				      self.info.get("curr"), "/", self.info.get("total"))
		elif self.mode == "属性粒度":
			if self.detail == 0:
				print("- 〔", self.mode, self.info.get('head'), "〕类目：", self.info.get('category'), "-", self.info.get('attribute'),
				      "@", self.info.get('main'), " Page: ", self.info.get("curr"), "/", self.info.get("total"))
			elif self.detail == 1:
				print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
				print("- 参数：〖", self.info.get('main'), "/", self.info.get('category'), "/", self.info.get('attribute'),
				      "/", self.info.get('device'), "/", self.info.get('seller'), "〗")
				print("- 细节：〔", self.info.get('head'), "〕 Max items: ", self.info.get('quantity'), " Page: ",
				      self.info.get("curr"), "/", self.info.get("total"))
	
	def parse_html(self, html):
		doc = pq(html)
		if self.mode=="品牌粒度" and self.info.get("head")=="热销商品榜":
			for item in doc(".ui-tab-contents tbody")("tr").items():
				if item("td:nth_child(5)").text() != ">99999%":
					amplitude = str(float('%.4f' % (float(item("td:nth_child(5)").text().replace("%", "")) / 100)))
				else:
					amplitude = "999.9999"
				if item("td:nth_child(5)")("span:nth_child(1)").attr("class") == "down":
					amplitude = "-" + amplitude
				if item("td:nth_child(3) a").attr("href"):  # 排除可能存在的店铺被删除的情况
					yield {
						"date": self.info['main'],
						"brand": self.info['brand'][:20],
						"rank": item("td:first_child").text()[:3],
						"itemId": item("td:nth_child(2) a").attr("href").split("id=")[1][:60],
						"sale": item("td:nth_child(4)").text().replace(",", "")[:10],
						"saleAmplitude": amplitude,
						"percentConversion": item("td:nth_child(6)").text().replace(",", "")[:6],
						"category": self.info["category"],
						"title": item("td:nth_child(2)").text().replace("'","`")[:100].split("\n")[0],
						"originalPrice": item("td:nth_child(2)").text()[:100].split("：")[-1].replace(",",""),
						"shopName": item("td:nth_child(3)").text().replace("'","`")[:60],
						"shopUrl": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
						"mainPicUrl": item("td:nth_child(2) a img").attr("src").split(".jpg")[0].
							              split("uploaded/")[1][:100],
						"bsUrl": item("td.op a").attr("href")[:255],}
		elif self.mode=="品牌粒度" and self.info.get("head")=="流量商品榜":
			for item in doc(".ui-tab-contents tbody")("tr").items():
				if item("td:nth_child(3) a").attr("href"):  # 排除可能存在的店铺被删除的情况
					yield {
						"date": self.info['main'],
						"brand": self.info['brand'][:20],
						"rank": item("td:first_child").text()[:3],
						"itemId": item("td:nth_child(2) a").attr("href").split("id=")[1][:60],
						"flowIndex": item("td:nth_child(4)").text().replace(",", "")[:10],
						"searchPopularity": item("td:nth_child(5)").text().replace(",", ""),
						"paymentNumber": item("td:nth_child(6)").text().replace(",", "")[:6],
						"title": item("td:nth_child(2)").text().replace("'","`")[:100].split("\n")[0],
						"originalPrice": item("td:nth_child(2)").text().split("：")[-1].replace(",",""),
						"shopName": item("td:nth_child(3)").text().replace("'","`")[:60],
						"shopUrl": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
						"mainPicUrl": item("td:nth_child(2) a img").attr("src").split(".jpg")[0].
							              split("uploaded/")[1][:100],
						"bsUrl": item("td.op a").attr("href")[:255], }
		elif self.mode=="行业粒度" and self.info.get("head")=="热销商品榜":
			for item in doc(".ui-tab-contents tbody")("tr").items():
				if item("td:nth_child(5)").text() != ">99999%":
					amplitude = str(float('%.4f' % (float(item("td:nth_child(5)").text().replace("%", "")) / 100)))
				else:
					amplitude = "999.9999"
				if item("td:nth_child(5)")(
						"span:nth_child(1)").attr("class") == "down":
					amplitude = "-" + amplitude
				if item("td:nth_child(3) a").attr("href"):  # 排除可能存在的店铺被删除的情况
					yield {
						"date": self.info['main'],
						"category": self.info["category"],
						"rank": item("td:first_child").text()[:3],
						"itemId": item("td:nth_child(2) a").attr("href").split("id=")[1][:60],
						"sale": item("td:nth_child(4)").text().replace(",", "")[:10],
						"saleAmplitude": amplitude,
						"percentConversion": item("td:nth_child(6)").text().replace(",", "")[:6],
						"title": item("td:nth_child(2)").text().replace("'","`")[:100].split("\n")[0],
						"originalPrice": item("td:nth_child(2)").text()[:100].split("：")[-1].replace(",",""),
						"shopName": item("td:nth_child(3)").text().replace("'","`")[:60],
						"shopUrl": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
						"mainPicUrl": item("td:nth_child(2) a img").attr("src").split(".jpg")[0].
							              split("uploaded/")[1][:100],
						"bsUrl": item("td.op a").attr("href")[:255],
						"1688Url": item("td.op div a").attr("href").split("fromOfferId=")[-1].split("#topoffer")[0][:60],}
		elif self.mode=="行业粒度" and self.info.get("head")=="流量商品榜":
			for item in doc(".ui-tab-contents tbody")("tr").items():
				if item("td:nth_child(3) a").attr("href"):  # 排除可能存在的店铺被删除的情况
					yield {
						"date": self.info['main'],
						"category": self.info["category"],
						"rank": item("td:first_child").text()[:3],
						"itemId": item("td:nth_child(2) a").attr("href").split("id=")[1][:60],
						"flowIndex": item("td:nth_child(4)").text().replace(",", "")[:10],
						"searchPopularity": item("td:nth_child(5)").text().replace(",", ""),
						"paymentNumber": item("td:nth_child(6)").text().replace(",", "")[:6],
						"title": item("td:nth_child(2)").text().replace("'","`")[:100].split("\n")[0],
						"originalPrice": item("td:nth_child(2)").text().split("：")[-1].replace(",",""),
						"shopName": item("td:nth_child(3)").text().replace("'","`")[:60],
						"shopUrl": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
						"mainPicUrl": item("td:nth_child(2) a img").attr("src").split(".jpg")[0].
							              split("uploaded/")[1][:100],
						"bsUrl": item("td.op a").attr("href")[:255],
						"1688Url": item("td.op div a").attr("href").split("fromOfferId=")[-1].split("#topoffer")[0][:60],}
		elif self.mode=="属性粒度":
			for item in doc(".ui-tab-contents tbody")("tr").items():
				if item("td:nth_child(3) a").attr("href"):  # 排除可能存在的店铺被删除的情况
					yield {
						"date": self.info['main'],
						# "category": self.info["category"],
						# "type": PERMIT_attribute[self.info["category"]][self.info["attribute"]],
						"attribute": self.info['attribute'],
						"rank": item("td:first_child").text()[:3],
						"itemId": item("td:nth_child(2) a").attr("href").split("id=")[1][:60],
						"sale": item("td:nth_child(4)").text().replace(",", "")[:10],
						"searchPopularity": item("td:nth_child(5)").text().replace(",", ""),
						"paymentNumber": item("td:nth_child(6)").text().replace(",", "")[:6],
						"title": item("td:nth_child(2)").text().replace("'","`")[:100].split("\n")[0],
						"originalPrice": item("td:nth_child(2)").text().split("：")[-1].replace(",",""),
						"shopName": item("td:nth_child(3)").text().replace("'","`")[:60],
						"shopUrl": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
						"mainPicUrl": item("td:nth_child(2) a img").attr("src").split(".jpg")[0].
							              split("uploaded/")[1][:100],
						"bsUrl": item("td.op a").attr("href")[:400], }
			
		
	def save_sql(self, result):
		centence = ""
		for item in result:
			centence += self.item_sql(item)
		for sql in SQL_LIST:
			data = self.sql_answer(sql, centence)
			print("   @ [{}]:\t{}".format(sql, data))
			
	
	def item_sql(self, item):
		sql_dict={}
		sql_dict.update({i[0]:i[1] for i in item.items() if i[0] in
		                 databases_config[self.mode][self.info["head"]]["item_list"]})
		# sql_dict.update({"createdDate": item["date"]})
		key_centence = ""
		value_centence = ""
		for key, value in sql_dict.items():
			key_centence += "`" + str(key) + "`" + ","
			value_centence += "'" + str(value) + "'" + ","
		table = databases_config[self.mode][self.info["head"]]["table"]
		if table == "bc_brand_granularity_sales" and (self.info["brand"] in OWNED_LIST):
			table = "bc_owned_granularity_sales"
		elif table == "bc_brand_granularity_visitor" and (self.info["brand"] in OWNED_LIST):
			table = "bc_owned_granularity_visitor"
		elif table == "bc_category_granularity":
			table = "bc_category_{}_{}".format(COMPARE_category[self.info["category"]],
			                COMPARE_type[PERMIT_attribute[self.info["category"]][self.info["attribute"]]])
		centence = "INSERT INTO `{}`({}) VALUES({});".format(table, key_centence[:-1], value_centence[:-1])
		return centence
		
	def sql_answer(self, sql, sql_centence):
		# 通用型mysql数据反馈，sql系数，sql语句
		data = ""
		conn = pymysql.connect(
			host=configure.echo(sql)["config"]["host"],
			port=configure.echo(sql)["config"]["port"],
			user=configure.echo(sql)["config"]["user"],
			passwd=configure.echo(sql)["config"]["passwd"],
			charset=configure.echo(sql)["config"]["charset"],
			db="baoersqlbs")
		try:
			cursor = conn.cursor()
			cursor.execute(sql_centence)
			conn.commit()
			data = cursor.fetchall()
			if not data:
				data = "Write completion!"    # 返回一个标记
		except Exception as e:
			conn.rollback()
			data = str(e)
		finally:
			cursor.close()
			conn.close()
		return data
	
	def check_sql(self):
		print("\n")
		if self.mode in ["行业粒度", "品牌粒度"]:
			for sql in SQL_LIST:
				# “行业粒度”/“品牌粒度”
				print("#" * 70)
				print(" #Check Switch# Mode: {} - Date: {} @ User: {}".format(self.mode, self.info["main"], sql))
				print("#" * 70)
				if self.mode == "行业粒度":
					table_list = ["bc_attribute_granularity_sales", "bc_attribute_granularity_visitor"]
					item_list = PERMIT["行业粒度"]
					item_name = "category"
				elif self.mode == "品牌粒度" and (self.brand_list[0] in BRAND_LIST):
					table_list = ["bc_brand_granularity_sales", "bc_brand_granularity_visitor", ]
					item_list = set(BRAND_LIST)
					item_name = "brand"
				elif self.mode == "品牌粒度" and (self.brand_list[0] in OWNED_LIST):
					table_list = ["bc_owned_granularity_sales", "bc_owned_granularity_visitor", ]
					item_list = set(OWNED_LIST)
					item_name = "brand"
				for item in item_list:
					for table in table_list:
						centence = "SELECT COUNT(*),MAX(`rank`) FROM {} WHERE `date`='{}' AND `{}`='{}';".format(table,
						                                                        self.info["main"], item_name, item)
						data = self.sql_answer(sql, centence)
						if int(data[0][0]) == 0:
							mark = "**"
						elif int(data[0][0]) < int(data[0][1]):
							mark = "!!!"
						else:
							mark = "v"
						print("   & {} & {} :\t\t{}\t {}".format(table.center(32), item[-7:].ljust(7),
						                                (str(data[0][0])+"/"+str(data[0][1])).rjust(7), mark))
		elif self.mode == "属性粒度":
			for sql in SQL_LIST:
				# 属性粒度
				print("#" * 70)
				print(" #Check Switch# Mode: {} - Date: {} @ User: {}".format(self.mode, self.info["main"], sql))
				print("#" * 70)
				for category in PERMIT["属性粒度"]:
					for style in PERMIT["属性粒度"][category]:
						for attribute in PERMIT["属性粒度"][category][style]:
							table = "bc_category_{}_{}".format(COMPARE_category[category], COMPARE_type[style])
							centence = "SELECT COUNT(*),MAX(`rank`) FROM {} WHERE `date`='{}' AND `attribute`='{}';".format(table,
						                                                                self.info["main"], attribute)
							data = self.sql_answer(sql, centence)
							if int(data[0][0]) == 0:
								mark = "**"
							elif int(data[0][0]) < int(data[0][1]):
								mark = "!!!"
							else:
								mark = "v"
							print("   & {} & {}:\t{}\t {}".format(table.center(26),(category+"-"+style+"-"+attribute).
							        center(14), (str(data[0][0])+"/"+str(data[0][1])).rjust(7), mark))
				
