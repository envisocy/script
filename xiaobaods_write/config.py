# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:47'

import os

######################
###### document ######
######################

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

# 品牌粒度列表
BRAND_LIST = [
	"PNVN", "冬朵", "凝享", "前途", "CHNPLUM/华梅", "呀吼", "好虫常在", "尚兰奴", "尚·蔓蒂", "尚驭", "左街右巷", "慕爱人",
    "梦觅", "橡树猫", "比丽福", "波世岛", "淑美林", "知心羊", "粉蝉", "艾妃尼思", "花嫉", "萌路", "蒙奴莎", "雅来特", "音棉",
]

# 自有店铺粒度列表(通过erp中的shop.query更新)
OWNED_LIST = [
	"芮丽娅", "zsrs", "rfzk",
]

# 更新OWNED_LIST列表
def return_shop_list(sql="xiaobaods_w"):
    import pymysql
    import configure
    conn = pymysql.connect(
        host=configure.echo(sql)["config"]["host"],
        port=configure.echo(sql)["config"]["port"],
        user=configure.echo(sql)["config"]["user"],
        passwd=configure.echo(sql)["config"]["passwd"],
        charset=configure.echo(sql)["config"]["charset"],
        db="baoersqlerp")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT `brand` FROM `shops.query` WHERE `operator` is not null;")
        conn.commit()
        data = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    result = [i[0] for i in data]
    return result
OWNED_LIST.extend(return_shop_list())



# 通行证
PERMIT = {
	"品牌粒度":["女装/女士精品", ],
	"行业粒度":["牛仔裤", "休闲裤", "打底裤", "半身裙", "棉裤/羽绒裤", "T恤", "卫衣/绒衫"],
	"属性粒度":{
			  "牛仔裤": {
				  "款式": ["哈伦裤", "阔脚裤", "铅笔裤", "连衣裤", "背带裤", "直筒", "灯笼裤", "微喇裤", "工装裤", "垮裤", ],
				  "裤长": ["长裤", "超短裤", "短裤", "五分裤", "九分裤", "七分裤",],
				  "腰型": ["低腰", "中腰", "高腰"],
				  "厚薄": ["超薄", "薄款", "常规", "加厚"],
						},
			  "打底裤": {
				  "厚薄": ["薄款", "常规", "加绒", "加厚"],
				  "裤长": ["长裤", "短裤", "七分裤/九分裤"],
						},
			},
		}


# 数据库对照名
COMPARE_category = {
	"牛仔裤": "jean",
	"打底裤": "legging",
	"休闲裤": "casual",
}

COMPARE_type = {
	"款式": "style",
	"裤长": "length",
	"腰型": "waist",
	"厚薄": "thick",
}


# 反向查询：PERMIT_attribute = {'打底裤': {'七分裤/九分裤': '裤长', '加厚': '厚薄',...}
PERMIT_attribute = {}
for category in PERMIT["属性粒度"]:
    PERMIT_attribute.update({category:{}})
    for style in PERMIT["属性粒度"][category]:
        for item in PERMIT["属性粒度"][category][style]:
            PERMIT_attribute[category].update({item:style})


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
	"属性粒度":{
		"热销商品榜":{
			"table":"bc_category_granularity",  # 替换
			"item_list":{"date", "attribute", "rank", "itemId", "sale", "searchPopularity",
			             "paymentNumber", "title", "originalPrice", "shopName",
			             "shopUrl", "mainPicUrl", "bsUrl",
			},
		},
	},
}


# ------------------------------
if not DESKTOP_DIR:
	DESKTOP_DIR = GetDesktopPath()

######################
###### pattern  ######
######################

TOP_LIST_WIN = ["D:\\download", "E:\\download", "G:\\download", \
                "D:\\搜狗高速下载", "E:\\搜狗高速下载", "G:\\搜狗高速下载",
                "H:\\download",]
TOP_LIST_LINUX = ["~/Downloads"]

SQL_LIST_PATTERN = [
	"xiaobaods_w",
	"localhost",
]
