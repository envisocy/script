# -*- coding: utf-8 -*-
#!/usr/bin/python

import os


### 默认的数据文件路径
default_file_path = "F:\测试文件"
default_file_path.replace("\\", os.sep)

### 默认的数据文件夹名
# 店铺财务文件夹
default_financial_store_folder = "店铺利润表"
# 供应商账单文件夹
default_vendor_bill_folder = "供应商账单"

### vendor中所有可识别的供应商及配置信息：
vendor_message = {
	"藏马": {"id": "078", "include": "藏马"},
	"爱裤者": {"id": "013", "include": "爱裤"},
	"主体酷": {"id": "011", "include": "主体"},
	"伊魅儿": {"id": "028", "include": "伊魅"},
	"小宋": {"id": "009", "include": "小宋", "format": 9},
	"小米女装": {"id": "001", "include": "小米女装", "format": 2},
	"小米": {"id": "008", "include": "小米", "except": "女装", "format": 2},
	"小美": {"id": "006", "include": "小美", "format": 8},
	"小安档口": {"id": "002", "include": "小安", "format": 2},
	"西部牛仔": {"id": "027", "include": "西部", "format": 5.1},
	"所遇": {"id": "025", "include": "所遇", "format": 2.1},
	"莎莎": {"id": "016", "include": "莎莎", "format": 2},
	"沙狼豹": {"id":	"017", "include": "沙狼豹", "format": 2},
	"米拉卡": {"id": "018", "include": "米拉卡", "format": 7},
	"玫瑰": {"id": "014", "include": "玫瑰", "format": 6},
	"迈纯": {"id": "020", "include": "迈纯", "except": "店", "format": 5},
	"迈纯二店": {"id": "021", "include": "迈纯二店", "format": 5.2},
	"款爱": {"id": "029", "include": "款爱"},
	"古德": {"id": "026", "include": "古德", "format": 4},
	"春雷": {"id": "030", "include": "春雷"},
	"创辉工厂": {"id": "096", "include": "创辉工厂", "format": 3},
	"创辉": {"id": "007", "include": "创辉", "except": "工厂", "format": 10},
	"百分百": {"id":	"012", "include": "百分百", "interpret": "bfb", "format": 2},
	"阿海": {"id": "023", "include": "阿海", "format": 1},
}