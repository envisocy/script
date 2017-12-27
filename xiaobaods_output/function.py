#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configure
import datetime
import pymysql
import pandas as pd

class basic():
    def __init__(self, **kwargs):

        self.sql = configure.echo(kwargs.get("sql", "xiaobaods_r"))["config"]
        # 基于数据库configure的选择
        self.sql["db"] = "baoersqlbasic"
        self.line_b = kwargs.get("line_b", 0)   # 最终输出条数起始
        self.line_f = kwargs.get("line_f", 20)   # 最终输出条数结束
        if self.line_b > self.line_f:
            self.line_b, self.line_f = self.line_f, self.line_b
        self.date = kwargs.get("date", datetime.datetime.today().date() -
                               datetime.timedelta(1))   # 抽出数据筛选日期
        self.category = kwargs.get("category", "牛仔裤")     # 抽出数据筛选“类目”
        self.length = kwargs.get("length", 7)     # 针对二次筛选需求的上溯天数
        self.table = kwargs.get("table", "")      # 具体的数据表，具体函数需指定
        self.variable = kwargs.get("variable", "热销排名")# 二次筛选需求的显示变量
        self.fillna = kwargs.get("fillna", "")  # 填充空值
        self.debug = kwargs.get("debug", 0)     # 选择输出项目
        self.path = kwargs.get("path","")       # debug=9,输出csv的路径指定
        self.keyword = kwargs.get("keyword","日期：")
        # 替换的关键词（防止显示数字在前的异常排序）
        self.screening = kwargs.get("screening",{})
        if self.screening:
            self.rankl = keargs.get["screening"].get("rankl", 0)
            self.rankm = keargs.get["screening"].get("rankm", 500)
            self.titler= keargs.get["screening"].get("titler", "")
            self.storer = keargs.get["screening"].get("storer", "")
            self.v1l = keargs.get["screening"].get("v1l", 99999999999)
            self.v1m = keargs.get["screening"].get("v1m", 0)
            self.v2l = keargs.get["screening"].get("v2l", 99999999999)
            self.v2m = keargs.get["screening"].get("v2m", 0)
            self.v3l = keargs.get["screening"].get("v3l", 99999999999)
            self.v3m = keargs.get["screening"].get("v3m", 0)
            self.v4l = keargs.get["screening"].get("v4l", 99999999999)
            self.v4m = keargs.get["screening"].get("v4m", 0)

    def run(self, fun="a"):
        self.xiaobaods_a()

    def request_date(self):
        try:
            conn = pymysql.connect(host=self.sql["host"],
                                  port=int(self.sql["port"]),
                                  user=self.sql["user"],
                                  passwd=self.sql["passwd"],
                                  charset=self.sql["charset"],
                                  db=self.sql["db"])
            cursor = conn.cursor()
            cursor.execute("SELECT min(`日期`),max(`日期`) from " + self.table +
                           " where `类目`='" + self.category + "';")
            date_limit = cursor.fetchall()
            date_floor = date_limit[0][0]
            date_ceiling = date_limit[0][1]
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
        if self.date > date_ceiling:
            self.date = date_ceiling
        if self.date < date_floor + datetime.timedelta (self.length - 1):
            self.date = date_floor + datetime.timedelta (self.length - 1)

    def request_df(self, sql, sql_total):
        try:
            conn = pymysql.connect(host=self.sql["host"],
                                  port=int(self.sql["port"]),
                                  user=self.sql["user"],
                                  passwd=self.sql["passwd"],
                                  charset=self.sql["charset"],
                                  db=self.sql["db"])
            total = pd.read_sql_query(sql_total, conn).iloc[0, 0]
            df = pd.read_sql_query(sql, conn)
            df["total"] = total
            conn.close()
        except Exception as e:
            print(e)
        if self.fillna == "bd":
            df = df.fillna(method="bfill", limit=1, axis=1)
            df.dropna(inplace=True)
        elif self.fillna == "drop":
            df.dropna(inplace=True)
        elif self.fillna == "":
            pass
        else:
            df = df.fillna(self.fillna)
        return df


    def xiaobaods_a(self):
        '''
        12-26-2017
        '''
        if self.table not in ["bc_attribute_granularity_sales",
                              "bc_attribute_granularity_visitor"]:
            self.table = "bc_attribute_granularity_sales"
        if self.table == "bc_attribute_granularity_sales":
            sql_select_f = "SELECT CT.`主图缩略图`,CT.`热销排名`,CT.`商品信息`, \
            CT.`所属店铺`,CT.`支付子订单数`,CT.`交易增长幅度`, CT.`支付转化率指数`,\
            CT.`宝贝链接`,CT.`店铺链接`,CT.`查看详情`,CT.`同款货源`"
            if self.variable not in ["热销排名", "支付子订单数", "交易增长幅度", \
                                     "支付转化率指数"]:
                self.variable = "热销排名"
        elif self.table == "bc_attribute_granularity_visitor":
            sql_select_f = "SELECT CT.`主图缩略图`,CT.`热销排名`,CT.`商品信息`, \
            CT.`所属店铺`,CT.`流量指数`,CT.`搜索人气`,CT.`支付子订单数`, \
            CT.`宝贝链接`, CT.`店铺链接`,CT.`查看详情`,CT.`同款货源`"
            if self.variable not in ["热销排名", "流量指数", "搜索人气",
                                     "支付子订单数"]:
                self.variable = "热销排名"
        self.request_date()
        # SQL
        sql_select_m = ""
        for i in range(self.length):
            sql_select_m += ",MAX(CASE ST.日期 WHEN " + str(self.date - \
                datetime.timedelta(self.length - i - 1)).replace("-", "") + \
                " THEN ST." + self.variable + " ELSE NULL END) AS `日期：" + \
                str(self.date - datetime.timedelta(self.length - i - 1)).
                replace("-", "") + "` "
        sql_select_re = ""
        if self.screening:
            sql_select_re = " AND CT.`热销排名`>=" + str(self.rankl) + \
                            " AND CT.`热销排名`<=" + str(self.rankm) + \
                " AND " + sql_select_f.split(",")[4] + "<=" + str(self.v1l) + \
                " AND " + sql_select_f.split(",")[4] + ">=" + str(self.v1m) + \
                " AND " + sql_select_f.split(",")[5] + "<=" + str(self.v2l) + \
                " AND " + sql_select_f.split(",")[5] + ">=" + str(self.v2m) + \
                " AND " + sql_select_f.split(",")[6] + "<=" + str(self.v3l) + \
                " AND " + sql_select_f.split(",")[6] + ">=" + str(self.v3m)
            if self.titler:
                sql_select_re += " AND CT.`商品信息` REGEXP('" +self.titler+"')"
            if self.storer:
                sql_select_re += " AND CT.`所属店铺` REGEXP('" +self.storer+"')"
        sql_select_b = "FROM " + self.table + " AS CT LEFT JOIN " +self.table+\
            " AS ST ON CT.`宝贝链接` = ST.`宝贝链接` WHERE CT.`日期` = " + \
            str(self.date).replace("-", "") + \
            " AND CT.类目 = '" + self.category + \
            "' AND ST.日期 >= " + str(self.date - \
            datetime.timedelta(self.length)).replace("-", "") + \
            " AND ST.类目 = '" + self.category + "'" + sql_select_re
        sql_select_e = " GROUP BY CT.`热销排名`,CT.`" + self.variable + \
            "` ORDER BY CT.`热销排名` LIMIT " + str(self.line_b) + "," + \
            str(self.line_f-self.line_b) + ";"
        sql_select_c = "SELECT COUNT(*) AS total FROM " + self.table + " AS CT \
            WHERE CT.`日期` = " + str(self.date).replace("-", "") + " AND \
            CT.类目 = '" + self.category + "'" + sql_select_re + ";"
        df = self.request_df(sql_select_f + sql_select_m + sql_select_b + \
                             sql_select_e, sql_select_c)
