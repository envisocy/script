#!usr/bin/env python3
# -*- coding:utf8 -*-

import numpy as np
import pandas as pd
import configure
from kpi_system.config import *
import datetime
import sys
import pymysql


class output:
    '''
    date: ep. "2017-12-01"
    department: [customer_service,]
    position: ["售前",]
    kpi_index:  {0:
                    {"weight": 权重乘数,
                     "name": 考核指标,
                     "varialbe": 权重变量,
                     "type": 计算方式: value 具体数值; range 数据范围; rank 排名;
                     "score": 具体分数范围}}
    '''
    def __init__(self, **kwargs):
        self.sql = configure.echo("xiaobaods_r")["config"]
        self.sql["db"] = "kpi_datebase"
        self.max_weight = kwargs.get("max_weight", 80)
        self.date = kwargs.get("date", datetime.datetime.strftime(datetime.datetime.now().date() - datetime.timedelta(30), "%Y-%m-01"))
        #if self.date.split("-")[-1] != "01":
        #    self.date = self.date[:-2] + "01"
        self.department = kwargs.get("department", "customer_service")
        self.table = department_table[self.department]
        self.position = kwargs.get("position", "售前")
        self.kpi_index = kwargs.get("kpi_index",
                    kpi_index_default[self.department + "#" + self.position])
        # 验证Kpi
        self.validation_data()

    def request_df(self, sql):
        '''
        输入 SQL 语句
        输出 df 表
        '''
        try:
            conn = pymysql.connect(host=self.sql["host"],
                                  port=int(self.sql["port"]),
                                  user=self.sql["user"],
                                  passwd=self.sql["passwd"],
                                  charset=self.sql["charset"],
                                  db=self.sql["db"])
            df = pd.read_sql_query(sql, conn)
            conn.close()
        except Exception as e:
            print(e)
            return None
        return df

    def validation_data(self):
        if not self.kpi_index:
            print(" - 缺失有效的Kpi机制！")
            sys.exit(" * 程序结束！")
        elif np.sum([ self.kpi_index[i]["weight"] for i in self.kpi_index]) !=\
                self.max_weight:
            ctl = input(" - Kpi总权重值不为100，是否继续？")
            if ctl != "y" and ctl != "Y":
                sys.exit(" * 程序结束！")

    def parse_ranking(self, expression, total, model="rank"):
        if model == "rank":
            li = [i+1 for i in range(total+1)]
            if "D" in expression:
                return []
            else:
                a1 = expression.split(":")[0]
                a2 = expression.split(":")[-1]
                a1 = int(a1) if a1 else 0
                if a1 > 0:
                    a1 -= 1
                a2 = int(a2) if a2 else len(li)
                if a2 < 0:
                    a2 += 1
                return li[a1:a2]
        elif model == "range":
            a1 = expression.split(":")[0]
            a2 = expression.split(":")[-1]
            a1 = float(a1) if a1 else 0
            a2 = float(a2) if a2 else 999999
            return [a1, a2]


    def kpi_parsing(self, df):
        number = 0
        df["总考核分"] = 0
        total = len(df) - 1
        for kpi_item in self.kpi_index:
            kpi = self.kpi_index[kpi_item]  # 简化字典
            number += 1 # 标号
            name = str(number) + "." + kpi["name"]  # 基础名
            df[name + "实际达成"] = 0
            df[name + "所属范围"] = ""
            df[name + "得分"] = 0
            df[name + "权重"] = kpi["weight"]
            df[name + "考核分"] = 0
        for line in range(len(df)):
            number = 0
            for kpi_item in self.kpi_index:
                kpi = self.kpi_index[kpi_item]  # 简化字典
                number += 1
                name = str(number) + "." + kpi["name"]  # 基础名
                if kpi["type"] == "value":
                    df.iloc[line, df.columns.tolist().index(name + "实际达成")] = kpi["reach"]
                    df.iloc[line, df.columns.tolist().index(name + "所属范围")] = kpi["extent"]
                    df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"]
                    df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"] * kpi["weight"]
                    df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"] * kpi["weight"]
                elif kpi["type"] == "rank":
                    for item in kpi["goal"]:
                        if df.iloc[line, df.columns.tolist().index(kpi["variable"])] in self.parse_ranking(item, total, kpi["type"]):    # total比实际值小 1
                            df.iloc[line, df.columns.tolist().index(name + "实际达成")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                            df.iloc[line, df.columns.tolist().index(name + "所属范围")] = item
                            df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"][item]
                            df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"][item] * kpi["weight"]
                            df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"][item] * kpi["weight"]
                elif kpi["type"] == "range":
                    for item in kpi["goal"]:
                        if df.iloc[line, df.columns.tolist().index(kpi["variable"])] >= self.parse_ranking(item, total, kpi["type"])[0] and df.iloc[line, df.columns.tolist().index(kpi["variable"])] < self.parse_ranking(item, total, kpi["type"])[1]:
                            df.iloc[line, df.columns.tolist().index(name + "实际达成")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                            df.iloc[line, df.columns.tolist().index(name + "所属范围")] = item
                            df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"][item]
                            df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"][item] * kpi["weight"]
                            df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"][item] * kpi["weight"]
        return df

    def return_kpi_rule(self):
        pass

    def return_table(self, name="", wangwang="", form="", date="", position=""):
        '''
        标准解析
        传入：姓名或姓名列表/ 旺旺或旺旺列表
        传出：标准列表
        '''
        if date:
            self.date = date
        if position:
            self.position = position
        sql = "SELECT * FROM " + self.table + " WHERE `日期`='" + self.date + \
        "' and `职位`='" + self.position + "';"
        df = self.request_df(sql)
        df = self.kpi_parsing(df)
        # 表格变换
        if name and wangwang:
            name = list(name)
            wangwang = list(wangwang)
            df = df.loc[df["姓名"].isin(name)|df["旺旺"].isin(wangwang), :]
        elif name:
            name = list(name)
            df = df.loc[df["姓名"].isin(name), :]
        elif wangwang:
            wangwang = list(wangwang)
            df = df.loc[df["旺旺"].isin(wangwang), :]
        # 输出格式
        if not form:
            return df
        elif form == "score":
            pass
