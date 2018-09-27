# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/9/25 11:53'

import os

# bs(1) 生意参谋取数设置

### 取数路径：
FILEDIR = ""
FILENAME = "html.txt"
### 数据库配置：
SQLLIST = [
	"xiaobaods_w",
	"localhost",
]

### 默认路径配置
def GetDesktopPath():
	return os.path.join(os.path.expanduser("~"), 'Desktop')

if not FILEDIR:
	FILEDIR = GetDesktopPath()

# form
### {...: {"content": 检验内容/"return"回调, "alias": 信息显示的文字内容, "text"/"mode"/"arg": 检验参数}}

FORMDIC = {
	"市场大盘": {
		"tag": {"content": "市场", "alias": "生意参谋主标签", "text": "ul.menu-list .selected", },
		"root": {"content": "女装/女士精品", "alias": "主分类", "text": ".isready .common-picker-header", "mode": "attr", "arg": "title", },
		"date": {"content": "return", "alias": "日期","text": ".oui-date-picker-current-date", "mode": "split", "arg": 1, },
		"time": {"content": "日", "alias":"时间周期", "text": "#app button.ant-btn-primary", },
		"terminal": {"content": "所有终端", "alias": "终端设备", "text": ".oui-select-container-value", },
		"pathform": {"content": "全部", "alias": "pathform", "text": ".ebase-FaCommonFilter__right .ant-select-selection-selected-value", },
		"number1": {"content": "100", "alias": "条目数1", "text": "#cateCons .ant-select-selection-selected-value", },
		"number2": {"content": "100", "alias": "条目数2", "text": "#cateOverview .ant-select-selection-selected-value", },
	},
}

def returnDoc(doc, text, mode='', arg=''):
	if mode == 'attr':
		return doc(text).attr(str(arg)).strip()
	elif mode == 'split':
		return doc(text).text().split()[int(arg)].strip()
	return doc(text).text().strip()

UPDATEDIC = {
	"市场大盘": ['date'],
}

TABLEDIC = {
	"市场大盘": {"table": "bs_market_quotations",},
}

SQL_LIST_PATTERN = [
	'xiaobaods_w',
	'localhost',
]