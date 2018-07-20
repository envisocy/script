#!usr/bin/env python
# -*- coding: utf-8 -*-


from pyquery import PyQuery as pq
from xiaobaods_input.Business_adviser_parser.config import MODE4_PERMIT
import requests


def mode(html):
    '''
    当前所有可处理的项目类型
    :param html:
    :return: mode
    '''
    doc = pq(html)
    mode = 0
    if doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
    ) == "品牌粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
        # 商品店铺榜 - 品牌粒度
        mode = 1
    elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".breadcrumb .active").text() == "商品详情":
        # 商品店铺榜 - 商品详情（商品详细数据）
        mode = 2
    elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
    ) == "行业粒度" and doc(".active.ui-tab-head-item").text() in ["热销商品榜", "流量商品榜"]:
        # 商品店铺榜 - 行业粒度
        mode = 3
    elif doc(".selected-mask").parent().text() == "商品店铺榜" and doc(".page-header-item.active").text(
    ) == "属性粒度" and doc(".active.ui-tab-head-item").text() == "热销商品榜":
        # 商品店铺榜 - 属性粒度
        mode = 4
    return mode


def main_split(msg):
    '''
    :param msg : msg['main'] = '%y-%m-%d~%y-%m-%d'
    :return msg : msg['main'] = '%y-%m-%d'
    '''
    if msg.get('main').split("~")[0] == msg.get('main').split("~")[1]:
        msg["main"] = msg.get('main').split("~")[0]
        return msg
    return None


def parse_content(mode, html):
    doc = pq(html)
    if mode == 1:
        return {
            "mask": "商品店铺榜",
            "header": "品牌粒度",
            "main": doc(".dtpicker-main-text .num").text().split("（")[1].split("）")[0],
            "category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
            "brand": doc(".brand-dropdown .btn.btn-dropdown").text(),
            "device": doc(".device-dropdown .btn.btn-dropdown").text(),
            "seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
            "head": doc(".active.ui-tab-head-item").text(),
            "quantity": doc(".config-selector .btn.btn-dropdown").text(),
            "curr": doc(".ui-pagination-curr").text(),
            "total": doc(".ui-pagination-total").text()[1]
        }
    elif mode == 2:
        if "tmall" in doc(".screen-header .item-panel .img-wrapper a").attr("href"): # 天猫
            try:
                shopname = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)(".slogo-shopname").text()
                shopurl = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)(".slogo-shopname").attr("href").split(".com")[0]+".com"
                brand = shopname.split("旗舰店")[0].split("专营店")[0].split("官方")[0].split("女装")[0].split("服饰")[0]
            except:
                shopname = "-"
                shopurl = "-"
                brand = "-"
        elif "taobao" in doc(".screen-header .item-panel .img-wrapper a").attr("href"): # 淘宝
            try:
                shopname = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)("strong a").attr("title")
                shopurl = pq(requests.get("http:" + doc(".screen-header .item-panel .img-wrapper a").attr("href")).text)("strong a").attr("href").split(".com")[0]+".com"
                brand = shopname
            except:
                shopname = "-"
                shopurl = "-"
                brand = "-"
        return {
            "mask": "商品店铺榜",
            "header": "商品详情",
            "main": doc(".dtpicker-main-text .num").text().split("（")[1].split("）")[0],
            "img": doc(".item-panel .img-wrapper img").attr("src"),
            "title": doc(".screen-header .item-panel").text().replace(" ",""),
            'href': (doc(".screen-header .item-panel .img-wrapper a").attr("href").split("?")[0] + "?id=" +\
doc(".screen-header .item-panel .img-wrapper a").attr("href").split("id=")[1])[:60],
            "id": doc(".screen-header .item-panel .img-wrapper a").attr("href").split("id=")[1],
            "shopname": shopname,
            "shopurl": shopurl,
            "brand": brand,
        }
    elif mode == 3:
        return {
            "mask": "商品店铺榜",
            "header": "行业粒度",
            "main": doc(".dtpicker-main-text .num").text().split("（")[1].split("）")[0],
            "category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
            "device": doc(".device-dropdown .btn.btn-dropdown").text(),
            "seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
            "head": doc(".active.ui-tab-head-item").text(),
            "quantity": doc(".config-selector .btn.btn-dropdown").text(),
            "curr": doc(".ui-pagination-curr").text(),
            "total": doc(".ui-pagination-total").text()[1]
        }
    elif mode == 4:
        return {
            "mask": "商品店铺榜",
            "header": "属性粒度",
            "main": doc(".dtpicker-main-text .num").text().split("（")[1].split("）")[0],
            "category": doc(".category-dropdown .btn.btn-dropdown").text().split(">")[-1],
            "attribute": doc(".flex-content").text(),
            "device": doc(".device-dropdown .btn.btn-dropdown").text(),
            "seller": doc(".seller-dropdown .btn.btn-dropdown").text(),
            "head": doc(".active.ui-tab-head-item").text(),
            "quantity": doc(".config-selector .btn.btn-dropdown").text(),
            "curr": doc(".ui-pagination-curr").text(),
            "total": doc(".ui-pagination-total").text()[1]
        }
    return None


def parse_main_control(mode, msg, html):
    if mode == 1:
        return parse_page_mode1(msg, html)
    if mode == 3:
        return parse_page_mode3(msg, html)
    if mode == 4:
        return parse_page_mode4(msg, html)
    return None


def parse_page_mode1(msg, html):
    doc = pq(html)
    if msg.get('head') == "热销商品榜":
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
                    "日期": msg['main'],
                    "品牌": msg['brand'][:10],
                    "热销排名": item("td:first_child").text()[:3],
                    "商品信息": item("td:nth_child(2)").text()[:100],
                    "所属店铺": item("td:nth_child(3)").text()[:60],
                    "店铺链接": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
                    "支付子订单数": item("td:nth_child(4)").text().replace(",", "")[:10],
                    "交易增长幅度": amplitude,
                    "支付转化率指数": item("td:nth_child(6)").text().replace(",", "")[:6],
                    "宝贝链接": (item("td:nth_child(2) a").attr("href").split("?")[0] + "?id=" +\
                        item("td:nth_child(2) a").attr("href").split("id=")[1])[:60],
                    "主图缩略图": item("td:nth_child(2) a img").attr("src")[:160],
                    "查看详情": "https://sycm.taobao.com/mq/industry/rank/brand.htm?spm=a21ag.7749237.0.0.7d79124647cLZN" + item("td.op a").attr("href")[:400]}
    elif msg.get('head') == "流量商品榜":
        for item in doc(".ui-tab-contents tbody")("tr").items():
            if item("td:nth_child(3) a").attr("href"):  # 可能存在的店铺被删除的情况
                yield {
                    "日期": msg['main'],
                    "品牌": msg['brand'][:10],
                    "热销排名": item("td:first_child").text()[:3],
                    "商品信息": item("td:nth_child(2)").text()[:100],
                    "所属店铺": item("td:nth_child(3)").text()[:60],
                    "店铺链接": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
                    "流量指数": item("td:nth_child(4)").text().replace(",", "")[:12],
                    "搜索人气": item("td:nth_child(5)").text().replace(",", "")[:10],
                    "支付子订单数": item("td:nth_child(6)").text().replace(",", "")[:10],
                    "宝贝链接": (item("td:nth_child(2) a").attr("href").split("?")[0] + "?id=" +\
                        item("td:nth_child(2) a").attr("href").split("id=")[1])[:60],
                    "主图缩略图": item("td:nth_child(2) a img").attr("src")[:160],
                    "查看详情": "https://sycm.taobao.com/mq/industry/rank/brand.htm?spm=a21ag.7749237.0.0.7d79124647cLZN" + item("td.op a").attr("href")[:400]}


def parse_page_mode2_0(msg, html):
    doc = pq(html)
    if "加载" in doc('.content').text():
        print("* 错误：录入数据不完整，存在未加载的情况，请刷新页面重新录入！")
        exit()
    for i in doc('.mod-item-flow-source .source-table-wrapper').items():
        for j in i('tbody tr').items():
            yield {
                "id": msg['id'][:13],
                "日期": msg['main'],
                "表单": i("h5").text().replace("端来源", "")[:2],
                "来源名称": j("td:nth_child(1)").text()[:60],
                "访客数": j("td:nth_child(2)").text().replace(",", "")[:12],
                "访客数占比": str(float('%.4f' % (float(j("td:nth_child(3)").text().replace("%", "")) / 100)))[:12],
                "浏览量": j("td:nth_child(4)").text().replace(",", "")[:12],
                "浏览量占比": str(float('%.4f' % (float(j("td:nth_child(5)").text().replace("%", "")) / 100)))[:12]}

def parse_page_mode2_1(msg, html):
    doc = pq(html)
    for i in doc('.mod-item-source-keyword .source-table-wrapper').items():
        for j in i('tbody tr').items():
            yield {
                "id": msg['id'][:13],
                "日期": msg['main'],
                "表头": i.parent().parent().parent()(".navbar-header").text()[:12].replace("Top10", "").replace("关键词", "")[:2],
                "表单": i("h5").text().replace("端关键词","")[:2],
                "关键词": j("td:nth_child(1)").text()[:30],
                "访客数": j("td:nth_child(2)").text().replace(",", "")[:12]}

def parse_page_mode2_2(msg, html):
    doc = pq(html)
    for i in doc('.mod-item-related').items():
        for j in i('tbody tr').items():
            yield{
                "id": msg['id'][:13],
                "日期": msg['main'],
                "排名": j("td:nth_child(1)").text(),
                "主图缩略图": j("td:nth_child(2) .item-panel .img-wrapper a img").attr("src")[:160],
                "宝贝链接": (j("td:nth_child(2) .item-panel .img-wrapper a").attr("href").split("?")[0] + "?id=" +\
                j("td:nth_child(2) .item-panel .img-wrapper a").attr("href").split("id=")[1])[:60],
                "商品信息": j("td:nth_child(2) .item-panel .info-wrapper").text() + \
                "价格：" + j("td:nth_child(3)").text(),
                "关联指数": j("td:nth_child(4)").text(),
        }

def parse_page_mode2_3(msg, html):
    doc = pq(html)
    # 维护索引列表
    yield{
        "日期": msg['main'],
        "id": msg['id'][:15],
        "所属店铺": msg['shopname'],
        "店铺链接": msg["shopurl"],
        "品牌": msg["brand"],
        "主图缩略图": msg["img"],
        "商品信息": msg["title"][:100],
        "宝贝链接": msg["href"],
    }


def parse_page_mode3(msg, html):
    doc = pq(html)
    if msg.get('head') == "热销商品榜":
        for item in doc(".ui-tab-contents tbody")("tr").items():
            if item("td:nth_child(5)").text() != ">99999%":
                amplitude = str(float('%.4f' % (float(item("td:nth_child(5)").text().replace("%", "")) / 100)))
            else:
                amplitude = "999.9999"
            if item("td:nth_child(5)")(
                    "span:nth_child(1)").attr("class") == "down":
                amplitude = "-" + amplitude
            if item("td:nth_child(3) a").attr("href"):
                yield {
                    "日期": msg['main'],
                    "类目": msg['category'].split(">")[-1][:10],
                    "热销排名": item("td:first_child").text()[:3],
                    "商品信息": item("td:nth_child(2)").text()[:100],
                    "所属店铺": item("td:nth_child(3)").text()[:60],
                    "店铺链接": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
                    "支付子订单数": item("td:nth_child(4)").text().replace(",", "")[:10],
                    "交易增长幅度": amplitude,
                    "支付转化率指数": item("td:nth_child(6)").text().replace(",", "")[:6],
                    "宝贝链接": (item("td:nth_child(2) a").attr("href").split("?")[0] + "?id=" +\
                        item("td:nth_child(2) a").attr("href").split("id=")[1])[:60],
                    "主图缩略图": item("td:nth_child(2) a img").attr("src")[:160],
                    "查看详情": "https://sycm.taobao.com/mq/industry/rank/brand.htm?spm=a21ag.7749237.0.0.7d79124647cLZN" + item("td.op a").attr("href")[:400],
                    "同款货源": "https:" + item("td.op div a").attr("href")[:300]}
    elif msg.get('head') == "流量商品榜":
        for item in doc(".ui-tab-contents tbody")("tr").items():
            if item("td:nth_child(3) a").attr("href"):
                yield {
                    "日期": msg['main'],
                    "类目": msg['category'].split(">")[-1][:10],
                    "热销排名": item("td:first_child").text()[:3],
                    "商品信息": item("td:nth_child(2)").text()[:100],
                    "所属店铺": item("td:nth_child(3)").text()[:60],
                    "店铺链接": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
                    "流量指数": item("td:nth_child(4)").text().replace(",", "")[:10],
                    "搜索人气": item("td:nth_child(5)").text().replace(",", ""),
                    "支付子订单数": item("td:nth_child(6)").text().replace(",", "")[:6],
                    "宝贝链接": (item("td:nth_child(2) a").attr("href").split("?")[0] + "?id=" +\
                        item("td:nth_child(2) a").attr("href").split("id=")[1])[:60],
                    "主图缩略图": item("td:nth_child(2) a img").attr("src")[:160],
                    "查看详情": "https://sycm.taobao.com/mq/industry/rank/brand.htm?spm=a21ag.7749237.0.0.7d79124647cLZN" + item("td.op a").attr("href")[:400],
                    "同款货源": "https:" + item("td.op div a").attr("href")[:300]}


def parse_page_mode4(msg, html):
    doc = pq(html)
    for item in doc(".ui-tab-contents tbody")("tr").items():
        if item("td:nth_child(3) a").attr("href"):
            yield {
                "日期": msg['main'],
                "类目": msg['category'].split(">")[-1][:10],
                "类型": MODE4_PERMIT[msg['category']][msg['attribute']],
                "属性": msg['attribute'],
                "热销排名": item("td:first_child").text()[:3],
                "商品信息": item("td:nth_child(2)").text()[:100],
                "所属店铺": item("td:nth_child(3)").text()[:60],
                "店铺链接": item("td:nth_child(3) a").attr("href").split("?")[0][:60],
                "支付子订单数": item("td:nth_child(4)").text().replace(",", "")[:10],
                "支付件数": item("td:nth_child(5)").text().replace(",", "")[:10],
                "支付转化率指数": item("td:nth_child(6)").text().replace(",", "")[:6],
                "宝贝链接": (item("td:nth_child(2) a").attr("href").split("?")[0] + "?id=" +\
                    item("td:nth_child(2) a").attr("href").split("id=")[1])[:60],
                "主图缩略图": item("td:nth_child(2) a img").attr("src")[:160],
                "验证标题": item("td:nth_child(2)").text()[:100],# 待删除
                "查看详情": "https://sycm.taobao.com/mq/industry/rank/brand.htm?spm=a21ag.7749237.0.0.7d79124647cLZN" + item(
                    "td.op a").attr("href")[:400]}
