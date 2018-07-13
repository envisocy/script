# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

import os
import re
from pyquery import PyQuery as pq
import requests

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
		self.msg = " *** 载入文档并初始化信息 ***\n * From: {}{}{}\n * Details: {} bytes ( {} Blocks )\n ***" \
		           " *** *** *** *** *** ***\n".format(DESKTOP_DIR, os.sep, filename, len(html), len(htmls))
		self.htmls = htmls

	def run(self):
		print(self.msg)
		for html in self.htmls:
			self.parse(html)    # 二级解析
			self.prompt_message()
			if self.error:
				print("-!" * 30 + "\n" + self.error + "\n" + "-!" * 30 + "\n")
				continue
	
	def parse(self, html):
		self.error = ""
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
			return

	
	def parse_content(self, doc):
		if self.mode == "品牌粒度":
			self.info={
				"mask": "商品店铺榜",
				"header": "品牌粒度",
				"main": doc(".dtpicker-main-text .num").text(),
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
				"brand": doc(".brand-dropdown .btn.btn-dropdown").text(),
				"device": doc(".device-dropdown .btn.btn-dropdown").text(),
				"seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
				"head": doc(".active.ui-tab-head-item").text(),
				"quantity": doc(".config-selector .btn.btn-dropdown").text(),
				"curr": doc(".ui-pagination-curr").text(),
				"total": doc(".ui-pagination-total").text(),
			}
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
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
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
				"category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
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
		self.info["total"] = self.info["total"][1]  # "共5页" 取页数数字
		# validation_message
		if self.info.get("category") not in  PERMIT[self.mode].get("category", []):
			self.error = " !!! 品类选择错误或超出范围，请检查后再试！此数据被忽略！"
		if self.info.get("attribute") not in PERMIT[self.mode].get("attribute", []) or self.info.get("attribute") \
				not in PERMIT[self.mode].get("attribute", []).get(self.info.get("category"), []):
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
				print("- 〔", self.info.get('header'), "〕日期：", self.info.get('brand'), "@", self.info.get('main'),
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
				print("- 〔", self.info.get('head'), "〕类目：", self.info.get('category'), "@", self.info.get('main'),
				      " Page: ", self.info.get("curr"), "/", self.info.get("total"))
			elif self.detail == 1:
				print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
				print("- 参数：〖", self.info.get('main'), "/", self.info.get('category'), "/", self.info.get('brand'),
				      "/", self.info.get('device'), "/", self.info.get('seller'), "〗")
				print("- 细节：〔", self.info.get('head'), "〕 Max items: ", self.info.get('quantity'), " Page: ",
				      self.info.get("curr"), "/", self.info.get("total"))
		elif self.mode == "属性粒度":
			if self.detail == 0:
				print("- 〔", self.info.get('head'), "〕类目：", self.info.get('category'), "-", self.info.get('attribute'),
				      "@", self.info.get('main'), " Page: ", self.info.get("curr"), "/", self.info.get("total"))
			elif self.detail == 1:
				print("- 目录：【", self.info.get('mask'), "-", self.info.get('header'), "】")
				print("- 参数：〖", self.info.get('main'), "/", self.info.get('category'), "/", self.info.get('attribute'),
				      "/", self.info.get('device'), "/", self.info.get('seller'), "〗")
				print("- 细节：〔", self.info.get('head'), "〕 Max items: ", self.info.get('quantity'), " Page: ",
				      self.info.get("curr"), "/", self.info.get("total"))
		
