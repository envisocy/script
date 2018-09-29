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
### Ver_0.2.3 加入 condition 字段，只有满足条件，才会触发 form 的停止机制

FORMDIC = {
	"市场大盘": {
		"tag": {"content": "市场", "alias": "生意参谋主标签", "text": "ul.menu-list .selected", },
		"root": {"content": "return", "alias": "主分类", "text": ".isready .common-picker-header", "mode": "attr", "arg": "title", },
		"date": {"content": "return", "alias": "日期","text": ".oui-date-picker-current-date", "mode": "split", "arg": 1, },
		"time": {"content": "日", "alias":"时间周期", "text": "#app button.ant-btn-primary", },
		"terminal": {"content": "所有终端", "alias": "终端设备", "text": ".oui-select-container-value", },
		"pathform": {"content": "全部", "alias": "pathform", "text": ".ebase-FaCommonFilter__right .ant-select-selection-selected-value", },
		"total1": {"content": "100", "alias": "条目数1", "text": "#cateCons .ant-select-selection-selected-value",
		           "condition": ["root", "女装/女士精品"]},
		"total2": {"content": "100", "alias": "条目数2", "text": "#cateOverview .ant-select-selection-selected-value",
		           "condition": ["root", "女装/女士精品"]},
	},
	"市场排行": {
		"tag": {"content": "市场", "alias": "生意参谋主标签", "text": "ul.menu-list .selected", },
		"root": {"content": "女装/女士精品", "alias": "主分类", "text": ".isready .common-picker-header", "mode": "attr", "arg": "title", },
		"date": {"content": "return", "alias": "日期","text": ".oui-date-picker-current-date", "mode": "split", "arg": 1, },
		"time": {"content": "日", "alias":"时间周期", "text": "#app button.ant-btn-primary", },
		"terminal": {"content": "所有终端", "alias": "终端设备", "text": ".oui-select-container-value", },
		"pathform": {"content": "全部", "alias": "pathform", "text": ".ebase-FaCommonFilter__right .ant-select-selection-selected-value", },
		"rankname": {"content": "return", "alias": "排行", "text": ".ebase-Switch__activeItem", },
		"ranktype": {"content": "return", "alias": "方式", "text": ".oui-tab-switch-item-active", },
		"total": {"content": "100", "alias": "条目数", "text": '.oui-card-content .ant-select-selection-selected-value', },
		"page": {"content": "return", "alias": "方式", "text": ".ant-pagination-item-active", },
	},
	"搜索排行": {
		"tag": {"content": "市场", "alias": "生意参谋主标签", "text": "ul.menu-list .selected", },
		"root": {"content": "return", "alias": "主分类", "text": ".isready .common-picker-header", "mode": "attr", "arg": "title", },
		"date": {"content": "return", "alias": "日期","text": ".oui-date-picker-current-date", "mode": "split", "arg": 1, },
		"time": {"content": "日", "alias":"时间周期", "text": "#app button.ant-btn-primary", },
		"terminal": {"content": "所有终端", "alias": "终端设备", "text": ".oui-select-container-value", },
		"rankname": {"content": "return", "alias": "排行", "text": ".ebase-Switch__activeItem", },
		"ranktype": {"content": "return", "alias": "方式", "text": ".oui-tab-switch-item-active", },
		"total": {"content": "100", "alias": "条目数", "text": '.oui-card-content .ant-select-selection-selected-value', },
		"page": {"content": "return", "alias": "方式", "text": ".ant-pagination-item-active", },
	},
}

def returnDoc(doc, text, mode='', arg=''):
	if mode == 'attr':
		return doc(text).attr(str(arg)).strip()
	elif mode == 'split':
		return doc(text).text().split()[int(arg)].strip()
	return doc(text).text().strip()

UPDATEDIC = {
	"市场大盘": ['root', 'date', ],
	"市场排行": ['date', ],
	"搜索排行": ['root', 'date', 'rankname' ],
}

SQL_LIST_PATTERN = [
	'xiaobaods_w',
	'localhost',
]


RANKDIC = {
	"市场大盘": {"title": ["category"], "table": "bs_market_quotations", },
	"店铺高交易": {"title": ["name", "rank", "trade_index", "trade_growth", "payment_conversion"],
	          "table": "bs_market_rank_shop_sale", },
	"店铺高流量": {"title": ["name", "rank", "flow_index", "search_popularity", "trade_index"],
	          "table": "bs_market_rank_shop_flow", },
	"商品高交易": {"title": ["name", "rank", "trade_index", "trade_growth", "payment_conversion"],
	          "table": "bs_market_rank_item_sale", },
	"商品高流量": {"title": ["name", "rank", "flow_index", "search_popularity", "trade_index"],
	          "table": "bs_market_rank_item_flow", },
	"商品高意向": {"title": ["name", "rank", "collection_popularity", "cart_popularity", "trade_index"],
	          "table": "bs_market_rank_item_desire", },
	"品牌高交易": {"title": ["name", "rank", "trade_index", "trade_growth", "payment_conversion"],
	          "table": "bs_market_rank_brand_sale", },
	"品牌高流量": {"title": ["name", "rank", "flow_index", "search_popularity", "trade_index"],
	          "table": "bs_market_rank_brand_flow", },
	"搜索词热搜": {"title": ["name", "rank", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_hot", },
	"长尾词热搜": {"title": ["name", "rank", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_hot", },
	"品牌词热搜": {"title": ["name", "rank", "relative_number", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_hot", },
	"核心词热搜": {"title": ["name", "rank", "relative_number", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_hot", },
	"修饰词热搜": {"title": ["name", "rank", "relative_number", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_hot", },
	"搜索词飙升": {"title": ["name", "rank", "rise_range", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_rise", },
	"长尾词飙升": {"title": ["name", "rank", "rise_range", "search_popularity", "click_populatity", "click_rate", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_rise", },
	"品牌词飙升": {"title": ["name", "rank", "rise_range", "relative_number", "search_popularity", "click_populatity", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_rise", },
	"核心词飙升": {"title": ["name", "rank", "rise_range", "relative_number", "search_popularity", "click_populatity", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_rise", },
	"修饰词飙升": {"title": ["name", "rank", "rise_range", "relative_number", "search_popularity", "click_populatity", "payment_conversion"],
	          "table": "bs_search_rank_searchwords_rise", },
}