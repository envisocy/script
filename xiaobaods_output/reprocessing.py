#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xiaobaods_output.basic
import numpy as np
import datetime
import pandas as pd
import pymysql
import configure
import sqlalchemy
import time
import os


class function():
    def __init__(self, **kwargs):
        self.sql = configure.echo(kwargs.get("sql", "xiaobaods_w"))["config"]
        self.sql["db"] = "baoersqlaftertreatment"
        self.line_b = kwargs.get("line_b", 1)
        self.line_f = kwargs.get("line_f", 5)
        self.fillna = kwargs.get("fillna", "")
        self.debug = kwargs.get("debug", 0)
        self.path = kwargs.get("path","")   # debug=9,输出csv的路径指定
        if not self.path:
            self.path = os.path.join(os.path.expanduser("~"),'Desktop')

    def run(self, fun="pr"):
        self.time_s = time.time()
        if fun == "pr":
            df = self.xiaobaods_pr()
        else:
            print(" * fun not be defined!")
        if self.debug == 6 or self.debug == 8:
            return df

    def request_df(self, sql, sql_total=""):
        df = None
        try:
            conn = pymysql.connect(host=self.sql["host"],
                                  port=int(self.sql["port"]),
                                  user=self.sql["user"],
                                  passwd=self.sql["passwd"],
                                  charset=self.sql["charset"],
                                  db=self.sql["db"])
            df = pd.read_sql_query(sql, conn)
            if sql_total:
                total = pd.read_sql_query(sql_total, conn).iloc[0, 0]
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
            '''
            算法接口，标题调整为序列
            '''
            return df
        elif self.debug == 7:
            print(df)
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

    def pr_df(self, date="", date_range=7, category="牛仔裤", alg="Dec"):
        df_total = pd.DataFrame()
        if date=="":
            date = datetime.datetime.strftime(datetime.datetime.now().
                date() - datetime.timedelta(1), "%Y-%m-%d")
        for series in range(date_range):
            date_end = datetime.datetime.strftime(datetime.datetime.
                                    strptime(date,"%Y-%m-%d").date() -
                                    datetime.timedelta(series), "%Y-%m-%d")
            print(" - - - " + str(series + 1) + "/" + str(date_range) +
                  "[" + alg + "]" + date_end)
            program = xiaobaods_output.basic.function(fun="a", date=date_end,
                                                    alg=alg, debug=8, line_f=500,
                                                     category=category)
            df = program.run()
            df.reset_index(drop=True, inplace=True)
            df["point"] = (-np.log((df.index+1)/20)+1) * (date_range -
                                                          series) / date_range
            df_total = pd.concat([df_total,df], axis=0)
        df_sort = df_total[["宝贝链接","point"]].groupby("宝贝链接",
                                            as_index=False,squeeze=True).sum()
        df_sort.sort_values("point", ascending=False, inplace=True)
        df_index = df_total[["主图缩略图", "商品信息", "所属店铺", "宝贝链接",
                "店铺链接", "查看详情", "同款货源"]].sort_values("宝贝链接").\
                drop_duplicates("宝贝链接")
        df_sort["date"] = date
        return pd.merge(df_sort, df_index, on="宝贝链接")

    def pr_input(self, date="", date_range=7, category_list=[], alg="Dec",
                 length=20):
        if not category_list:
            category_list = ["牛仔裤", "打底裤", "休闲裤"]
        for category in category_list:
            print(" - " + category)
            df = self.pr_df(date=date, date_range=date_range, alg="Dec")
            df["category"] = category
            df["alg"] = alg
            df["rank"] = df.index + 1
            df = df[:20]
            print(" - " + "to_sql")

            try:
                conn = pymysql.connect(host=self.sql["host"],
                                        port=int(self.sql["port"]),
                                        user=self.sql["user"],
                                        passwd=self.sql["passwd"],
                                        charset=self.sql["charset"],
                                        db=self.sql["db"])
            except pymysql.err.OperationalError as e:
                print("Error is " + str(e))

            try:
                engine = sqlalchemy.create_engine("mysql+pymysql://" +
                    self.sql["user"] + ':' + self.sql["passwd"] + "@" +
                    self.sql["host"] + ":" + str(self.sql["port"]) + "/" +
                    self.sql["db"] + "?charset=utf8")
            except sqlalchemy.exc.OperationalError as e:
                print('Error is '+str(e))
                sys.exit()
            except sqlalchemy.exc.InternalError as e:
                print('Error is '+str(e))
                sys.exit()

            df.to_sql(name='attribute_granularity_al_rank', con=engine,
                      if_exists='append', index=False)
            conn.close()


    def xiaobaods_pr(self, date="", category="牛仔裤", alg="Dec"):
        '''
        查询增长表: baoersqlaftertreatment.attribute_granularity_al_rank
        '''
        self.sql["db"] = "baoersqlaftertreatment"
        table = "attribute_granularity_al_rank"
        if not date:
            date = datetime.datetime.strftime(datetime.datetime.now().date() -
                                            datetime.timedelta(1), "%Y-%m-%d")
        SQL = "SELECT * From " + table + " WHERE `date`='" + date + "' AND \
        `category`='" + category + "' AND `alg`='" + alg + "' AND `rank`>=" + \
        str(self.line_b) + " AND `rank`<=" + str(self.line_f) + ";"
        df = self.request_df(SQL)
        return self.export(df=df,
                    msg="- date: " + date + "\n- category: " + category + "\n\
                    -alg: " + alg + "\n-rank: (" + str(self.line_b) + "," + \
                    str(self.line_f) + ")\n",
                    sql="- SQL: " + SQL,
                    filename="[DataGroup]" + table + "_" + category + "_" +
                    alg + "_" + date + "(" + str(self.line_b) + "," +
                    str(self.line_f) + ")",)
