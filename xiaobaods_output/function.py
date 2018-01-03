#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configure
import datetime
import pymysql
import numpy as np
import pandas as pd
import time
import json
import os


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
        self.path = kwargs.get("path","")   # debug=9,输出csv的路径指定
        if not self.path:
            self.path = os.path.join(os.path.expanduser("~"),'Desktop')
        self.keyword = kwargs.get("keyword","日期：")
        # 替换的关键词（防止显示数字在前的异常排序）
        self.rankl = kwargs.get("rankl", 0)
        self.rankm = kwargs.get("rankm", 500)
        self.titler= kwargs.get("titler", "")
        self.storer = kwargs.get("storer", "")
        self.v1l = kwargs.get("v1l", 99999999999)
        self.v1m = kwargs.get("v1m", 0)
        self.v2l = kwargs.get("v2l", 99999999999)
        self.v2m = kwargs.get("v2m", 0)
        self.v3l = kwargs.get("v3l", 99999999999)
        self.v3m = kwargs.get("v3m", 0)
        self.v4l = kwargs.get("v4l", 99999999999)
        self.v4m = kwargs.get("v4m", 0)
        self.alg = kwargs.get("alg", {})
        # 算法部分
        self.alg = kwargs.get("alg","")
        self.alpha = kwargs.get("alpha", 1.2)
        self.beta = kwargs.get("beta", 0.2)
        self.gamma = kwargs.get("gamma", 10)
        self.delta = kwargs.get("delta", 0.05)
        self.epsilon = kwargs.get("epsilon", 350)
        self.zeta = kwargs.get("zeta", 0)

    def run(self, fun="a"):
        self.time_s = time.time()
        if fun == "a":
            if not self.alg:
                df = self.xiaobaods_a()
            else:
                df = self.xiaobaods_a_alg()
        else:
            print(" * fun not be defined!")
        if self.debug == 6 or self.debug == 8:
            return df

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

    def export(self, df, msg, sql, filename=""):
        if self.debug == 1:
            print("- Running time：%.4f s" % (time.time() - self.time_s))
            print(msg)
        elif self.debug == 2:
            print("- Running time：%.4f s" % (time.time() - self.time_s))
            print(sql)
        elif self.debug == 6:
            return df
        elif self.debug == 8:
            return df
        elif self.debug == 9:
            print("- Running time：%.4f s" % (time.time() - self.time_s))
            try:
                df.to_csv(self.path + os.path.sep + filename + ".csv")
                print("> 输出CSV文件：", self.path, os.path.sep , filename)
            except Exception as e:
                print("> 输出CSV文件失败，错误原因：", e)
        else:
            print(df.to_json(orient="index"))

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
        debug_6_count = 0
        for i in range(self.length):
            if self.debug != 6:
                sql_select_m += ",MAX(CASE ST.日期 WHEN " + str(self.date - \
                datetime.timedelta(self.length - i - 1)).replace("-", "") + \
                " THEN ST." + self.variable + " ELSE NULL END) AS `" + \
                self.keyword + str(self.date - datetime.timedelta(self.length -\
                                        i - 1)).replace("-", "") + "` "
            else:
                debug_6_count += 1
                sql_select_m += ",MAX(CASE ST.日期 WHEN " + str(self.date - \
                datetime.timedelta(self.length - i - 1)).replace("-", "") + \
                " THEN ST." + self.variable + " ELSE NULL END) AS `" + \
                                        str(debug_6_count) + "` "
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
        sql_select = sql_select_f + sql_select_m + sql_select_b + sql_select_e
        df = self.request_df(sql_select, sql_select_c)
        return self.export(df=df,
                    msg="- date: " + datetime.datetime.strftime(self.date, \
                                                        "%m%d") + "\n" +
                        "- category: " + self.category + "\n" +
                        "- length: " + str(self.length) + "\n" +
                        "- page: " + str(df["total"][0]) + "[" + \
                        str(self.line_b) + "," + str(self.line_f) + "]\n" +
                        "- table: " + self.table + "\n" +
                        "- variable: " + self.variable + "\n" +
                        "- debug:" + str(self.debug) + "\n" +
                        "- fillna:" + self.fillna + "\n" +
                        "- path:" + self.path + "\n" +
                        "- keyword:" + self.keyword + "\n",
                    sql="- SQL: " + sql_select + "\n" +
                        "- SQL_total: " + sql_select_c,
                    filename="[DataGroup]" + self.table.split("_")[-1] + "_" +
                             self.category + "_Top500_" + self.variable + "_" +
                             datetime.datetime.strftime(self.date, "%m%d") +
                             str(self.length) + "(" + str(self.line_b) + "," +
                              str(self.line_f) + ")" )

    def xiaobaods_a_alg(self):
        if self.alg == "Dec":
            '''
            parameter
                - alpha 排名内权重内参数 默认1.2
                - beta 方差系数 默认0.2
                - gamma 拟合度系数 默认10
                - delta r2 系数 默认0.05
                - epsilon 排名权重系数 默认350
            '''
            # 排序表
            debug = 6
            line_b = 1
            line_f = 500
            length = 5
            self.alg = ""
            self.length, length = length, self.length
            self.line_b, line_b = line_b, self.line_b
            self.line_f, line_f = line_f, self.line_f
            self.debug, debug = debug, self.debug
            df = self.run().dropna()
            # std
            self.variable = "支付转化率指数"
            df_std = self.run().dropna()
            # 还原参数
            self.debug, debug = debug, self.debug
            self.length, length = length, self.length
            self.line_b, line_b = line_b, self.line_b
            self.line_f, line_f = line_f, self.line_f
            self.variable = "算法Dec"     # 仅考虑输出文档命名，如遇异常修改
            df_std["std"] = np.std(df_std.loc[:,["1","2","3","4","5"]], axis=1)
            df_std = df_std.loc[:,["宝贝链接", "std"]]
            # 合并
            df = pd.merge(df,df_std)
            df["lxx"] = 10
            df["lyy"] = (np.square(df.loc[:,"1"]) + np.square(df.loc[:,"2"]) + \
                np.square(df.loc[:,"3"])+ np.square(df.loc[:,"4"])+ \
                np.square(df.loc[:,"5"])) - np.square(df.loc[:,"1"] + \
                df.loc[:,"2"]+ df.loc[:,"3"]+ df.loc[:,"4"]+ df.loc[:,"5"])/5
            df["lxy"] = ( df.loc[:,"1"] + df.loc[:,"2"] * 2 + \
                         df.loc[:,"3"] * 3 + df.loc[:,"4"] * 4 + \
                         df.loc[:,"5"] * 5 ) - (df.loc[:,"1"] + \
                        df.loc[:,"2"] + df.loc[:,"3"] + df.loc[:,"4"] + \
                        df.loc[:,"5"]) * 3
            # 参数
            df["r2"] = df["lxy"]/df["lxx"] * -1
            df["br"] = np.square(df["lxy"]/np.sqrt(df["lxx"] * df["lyy"]))
            df["weg"] = 1/(df.loc[:,"5"] ** self.alpha)
            df["score"] = (df.loc[:, "std"] * self.beta + df.loc[:, "br"] *\
                self.gamma) * df.loc[:, "r2"] * self.delta * \
                df.loc[:, "weg"] * self.epsilon
            df.sort_values(by=["score"], ascending=False ,inplace=True)
            # line_b/f
            df = df.iloc[self.line_b: self.line_f]
            return self.export(df=df,
                        msg="- date: " + datetime.datetime.strftime(self.date, \
                                                            "%m%d") + "\n" +
                            "- category: " + self.category + "\n" +
                            "- length: " + str(self.length) + "\n" +
                            "- page: " + str(df["total"][0]) + "[" + \
                            str(self.line_b) + "," + str(self.line_f) + "]\n" +
                            "- table: " + self.table + "\n" +
                            "- variable: " + self.variable + "\n" +
                            "- debug:" + str(self.debug) + "\n" +
                            "- fillna:" + self.fillna + "\n" +
                            "- path:" + self.path + "\n" +
                            "- keyword:" + self.keyword + "\n",
                        sql="- SQL: None",
                        filename="[DataGroup]" + self.table.split("_")[-1] + "_" +
                                 self.category + "_Top500_" + self.variable + "_" +
                                 datetime.datetime.strftime(self.date, "%m%d") +
                                 str(self.length) + "(" + str(self.line_b) + "," +
                                  str(self.line_f) + ")" )
        else:
            return None
