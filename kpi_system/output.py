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
                     "type": 计算方式:
                        - value 具体数值;
                        - multiplier 乘数;
                        - range 数据范围;
                        - rank 排名;
                        - times 重复次数;
                     "score": 具体分数范围}}
    '''

    def __init__(self, **kwargs):
        self.sql = configure.echo("xiaobaods_r")["config"]
        self.sql["db"] = "kpi_datebase"
        self.max_weight = kwargs.get("max_weight", 100)
        self.date = kwargs.get("date",
                datetime.datetime.strftime(datetime.datetime.now().date() -
                                           datetime.timedelta(30), "%Y-%m-01"))
        if self.date.split("-")[-1] != "01":
            self.date = self.date[:-2] + "01"
        self.department = kwargs.get("department", "customer_service")
        self.table = department_table[self.department]
        self.position = kwargs.get("position", "售前")
        self.kpi_index = kwargs.get("kpi_index",
                    kpi_index_default[self.department + "#" + self.position])
        # 验证 Kpi
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
            if "D" in expression or "T" in expression:
                return []
            else:
                a1 = expression.split(":")[0]
                a2 = expression.split(":")[-1]
                a1 = int(a1) if a1 else 0
                if a1 > 0:
                    a1 -= 1
                a2 = int(a2) if a2 else len(li)
                if a2 <= 0:
                    a2 += 1
                return li[a1:a2]
        elif model in ["range", "times", "percentage"]:
            a1 = expression.split(":")[0]
            a2 = expression.split(":")[-1]
            a1 = float(a1) if a1 else 0
            a2 = float(a2) if a2 else 999999
            if model == "times":
                a1 -= 0.01
                a2 += 0.01
            if model == "percentage":
                a1 /= 100
                a2 /= 100
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
                elif kpi["type"] == "multiplier":
                    df.iloc[line, df.columns.tolist().index(name + "实际达成")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                    df.iloc[line, df.columns.tolist().index(name + "所属范围")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                    df.iloc[line, df.columns.tolist().index(name + "得分")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                    df.iloc[line, df.columns.tolist().index(name + "考核分")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])] * kpi["weight"]
                    df.iloc[line, df.columns.tolist().index("总考核分")] += df.iloc[line, df.columns.tolist().index(kpi["variable"])] * kpi["weight"]
                elif kpi["type"] == "rank":
                    for item in kpi["goal"]:
                        if df.iloc[line, df.columns.tolist().index(kpi["variable"])] in self.parse_ranking(item, total, kpi["type"]):    # total比实际值小 1
                            df.iloc[line, df.columns.tolist().index(name + "实际达成")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                            df.iloc[line, df.columns.tolist().index(name + "所属范围")] = item
                            df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"][item]
                            df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"][item] * kpi["weight"]
                            df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"][item] * kpi["weight"]
                elif kpi["type"] in ["range","times"]:
                    for item in kpi["goal"]:
                        if df.iloc[line, df.columns.tolist().index(kpi["variable"])] >= self.parse_ranking(item, total, kpi["type"])[0] and df.iloc[line, df.columns.tolist().index(kpi["variable"])] < self.parse_ranking(item, total, kpi["type"])[1]:
                            df.iloc[line, df.columns.tolist().index(name + "实际达成")] = df.iloc[line, df.columns.tolist().index(kpi["variable"])]
                            df.iloc[line, df.columns.tolist().index(name + "所属范围")] = item
                            df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"][item]
                            df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"][item] * kpi["weight"]
                            df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"][item] * kpi["weight"]
                elif kpi["type"] == "percentage":
                    for item in kpi["goal"]:
                        if df.iloc[line, df.columns.tolist().index(kpi["variable"])] >= self.parse_ranking(item, total, kpi["type"])[0] and df.iloc[line, df.columns.tolist().index(kpi["variable"])] < self.parse_ranking(item, total, kpi["type"])[1]:
                            df.iloc[line, df.columns.tolist().index(name + "实际达成")] = str(format(float(df.iloc[line, df.columns.tolist().index(kpi["variable"])])*100,".2f"))+"%"
                            if not item.split(":")[0]:
                                itemp = item + "%"
                            elif not item.split(":")[-1]:
                                itemp = item[:-2] + "%:"
                            else:
                                itemp = item.split(":")[0] + "%:" + item.split(":")[-1] + "%"
                            df.iloc[line, df.columns.tolist().index(name + "所属范围")] = itemp
                            df.iloc[line, df.columns.tolist().index(name + "得分")] = kpi["goal"][item]
                            df.iloc[line, df.columns.tolist().index(name + "考核分")] = kpi["goal"][item] * kpi["weight"]
                            df.iloc[line, df.columns.tolist().index("总考核分")] += kpi["goal"][item] * kpi["weight"]
        return df

    def rule(self):
        df = pd.DataFrame(columns=["序号", "考核指标", "考核标准",
                                "权重", "0", "0.6", "0.8", "1.0", "1.2", "1.5"])
        for i in self.kpi_index:
            df.loc[i, "序号"] = i
            df.loc[i, "考核指标"] = self.kpi_index[i]['name']
            df.loc[i, "考核标准"] = self.kpi_index[i]['variable']
            df.loc[i, "权重"] = self.kpi_index[i]['weight']
            df.fillna("", inplace=True)
            if self.kpi_index[i]['type'] in ["range", "rank", "times", "percentage"]:
                for j in self.kpi_index[i]['goal']:
                    if self.kpi_index[i]['goal'][j] == 1:
                        key_word = "1.0"
                    else:
                        key_word = str(self.kpi_index[i]['goal'][j])
                    j = j.replace(":", "~")
                    if not j.split("~")[-1]:
                        df.loc[i, key_word] = j.replace("~", "+")
                    elif not j.split("~")[0]:
                        df.loc[i, key_word] = j[1:] + "-"
                    else:
                        df.loc[i, key_word] = j
                    if self.kpi_index[i]['type'] == "percentage":
                        if df.loc[i, key_word][-1] in ["+", "-"]:
                            df.loc[i, key_word] = df.loc[i, key_word][:-2] + "%" + df.loc[i, key_word][-1]
                        else:
                            df.loc[i, key_word] = df.loc[i, key_word].split("~")[0] + "%~" + df.loc[i, key_word].split("~")[-1] + "%"
            elif self.kpi_index[i]['type'] == "value":
                df.loc[i, "1.0"] = self.kpi_index[i]["extent"]
            elif self.kpi_index[i]['type'] == "multiplier":
                df.loc[i, "1.0"] = "/"
        return df

    def sheet(self, name="", wangwang="", form="", date="", position=""):
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
        if form == "score":
            column_list = ["姓名"]
            column_list.extend([i for i in filter(lambda x:"考核分" in x,
                                                  df.columns.tolist())])
            return df.loc[: , column_list]
        elif not form or form == "all":
            return df
        else:
            column_list = ["姓名"]
            column_list.extend([i for i in filter(lambda x:form in x,
                                                  df.columns.tolist())])
            return df.loc[: , column_list]

    def analysis(self, name="", wangwang="", date="", position=""):
        df = self.sheet(name=name, wangwang=wangwang, form="score",
                        date=date, position=position)
        return df.describe()

    def to_csv(self, path="", filename="kpi.csv", name="", wangwang="",
               form="score", date="", position="", encoding="gbk"):
        import os
        if not path:
            path = os.path.join(os.path.expanduser("~"), 'Desktop')
        df = self.sheet(name=name, wangwang=wangwang, form=form, date=date,
                        position=position)
        pd.set_option('precision', 2)
        df.to_csv(path + os.sep + filename, encoding=encoding)
