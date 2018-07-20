# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:47'

import os

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

# 解析模块设置
### 默认桌面路径(或指定html.txt所在路径)
DESKTOP_DIR = ""
FILENAME = "html.txt"


# 数据库列表from configure
SQL_LIST = [
	"xiaobaods_w",
	"localhost",
]


# 通行证
PERMIT = {
	"品牌粒度":{"category": ["女装/女士精品", ]},
	"行业粒度":{"category": {"牛仔裤": None,
	                        "休闲裤": None,
	                        "打底裤": None,
	                        "半身裙": None, },},
	"属性粒度":{"category":{"牛仔裤", "打底裤",
	},
			  "attribute": {
	"牛仔裤": {
		'哈伦裤': "款式",
		'阔脚裤': "款式",
		'铅笔裤': "款式",
		'连衣裤': "款式",
		'背带裤': "款式",
		'直筒': "款式",
		'灯笼裤': "款式",
		'微喇裤': "款式",
		'工装裤': "款式",
		'垮裤': "款式",
		'长裤': "裤长",
		'超短裤': "裤长",
		'短裤': "裤长",
		'五分裤': "裤长",
		'九分裤': "裤长",
		'七分裤': "裤长",
		'高腰': "腰型",
		'低腰': "腰型",
		'中腰': "腰型",
		'超薄': "厚薄",
		'薄款': "厚薄",
		'常规': "厚薄",
		'加厚': "厚薄"},
	"打底裤": {
		'薄款': "厚薄",
		'常规': "厚薄",
		'加绒': "厚薄",
		'加厚': "厚薄",
		'长裤': "裤长",
		'短裤': "裤长",
		'七分裤/九分裤': "裤长"}}},
}


# 数据库配置
databases_config = {
	"行业粒度":{
		"热销商品榜":{"table":"bc_attribute_granularity_sales",
		            "item_list":{"date", "category", "rank", "itemId", "title", "shopName", "shopUrl",
		                         "sale", "saleAmplitude", "percentConversion", "mainPicUrl", "originalPrice",
		                         "bsUrl", "1688Url",},},
		"流量商品榜":{"table":"bc_attribute_granularity_visitor",
		            "item_list":{"date", "category", "rank", "itemId", "title", "shopName", "shopUrl",
		                         "flowIndex", "searchPopularity", "paymentNumber", "mainPicUrl", "originalPrice",
		                         "bsUrl", "1688Url",},},
	},
	"品牌粒度":{
		"热销商品榜":{"table":"bc_brand_granularity_sales",
		            "item_list":{"date", "brand", "rank", "itemId", "title", "shopName", "shopUrl",
		                         "sale", "saleAmplitude", "percentConversion", "mainPicUrl", "originalPrice",
		                         "bsUrl",},},
		"流量商品榜":{"table":"bc_brand_granularity_visitor",
		            "item_list":{"date", "brand", "rank", "itemId", "title", "shopName", "shopUrl",
		                         "flowIndex", "searchPopularity", "paymentNumber", "mainPicUrl", "originalPrice",
		                         "bsUrl",},},
	},
}


### shop_list
# shop_list_COLUMNS = [
# 	"shopUrl", "shopName", "brand", "location", "company",
# ]

item_list_COLUMNS = [
	"itemId", "category", "createdDate", "bsUrl", "1688Url", "originalPrice", "shopUrl", "shopName",
]

item_info_COLUMNS = [
	"itemId", "title", "mainPicUrl", "mainPicPhoneUrl", "originalPrice",
]

item_info_COLUMNS_check = [
	"title", "mainPicUrl", "originalPrice", "sellingPrice",
]

write_brand_granularity_sales = [
	"date", "brand", "rank", "itemId", "sale", "saleAmplitude", "percentConversion",
]

write_brand_granularity_visitor = [
	"date", "brand", "rank", "itemId", "flowIndex", "searchPopularity", "paymentNumber",
]

write_attribute_granularity_sales = [
	"date", "category", "rank", "itemId", "sale", "saleAmplitude", "percentConversion",
]

write_attribute_granularity_visitor = [
	"date", "category", "rank", "itemId", "flowIndex", "searchPopularity", "paymentNumber",
]

# ------------------------------
if not DESKTOP_DIR:
	DESKTOP_DIR = GetDesktopPath()