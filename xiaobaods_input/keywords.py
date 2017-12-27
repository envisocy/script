
#!usr/bin/env python
# -*- coding:utf-8 -*-

import os
from xiaobaods_input.config import *
import pandas as pd
import shutil
import sys
import pymysql


if "win" in sys.platform:
    top_list = top_list_win
elif "linux" in sys.platform:
    top_list = top_list_linux
else:
    top_list = []

def walk_list():
    date_list = {}
    for floder in top_list:
        try:
            for filename in os.listdir(floder):
                if "生意参谋" in filename:
                    if filename[8:18] not in date_list:
                        date_list[filename[8:18]] = set()
                    date_list[filename[8:18]].add(floder + os.path.sep + filename)
        except:
            pass
    return date_list

def check_date_list(date_list):
    for date_set in date_list:
        if len(date_list[date_set]) == 30:
            print(" * 处理", date_set, "中...")
            write_to_sql(date_list[date_set])
            print(" * 处理", date_set, "完毕!")
        else:
            print(" # ", date_set, "文档缺失，请确认后重新处理！")

def write_to_sql(filenames, sql_list=["localhost", "xiaobaods_w"]):
    import configure
    for filename in filenames:
        sql_insert = ""
        df= pd.read_excel(filename, header=3)
        print(filename)
        for r in range(len(df)):
            basename = os.path.basename(filename)
            sql_colunms ="(日期,类目,渠道,字段,"
            sql_values ="('"+basename[8:18]+"','"+basename[29:32]+"','"+basename[39:43]+"','"+basename[33:38]+"',"
            for s in df.columns:
                if s != df.columns[-1]:
                    if s == "词均支付转化率":
                        sql_colunms += "支付转化率,"
                        sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
                    elif s == "词均点击率":
                        sql_colunms += "点击率,"
                        sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
                    else:
                        sql_colunms += str(s)+","
                        sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
                else:
                    sql_colunms += str(s)
                    sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"'"
            if "热搜" in filename:
                sql_insert += "insert into bc_searchwords_hotwords " + sql_colunms + ") values" + sql_values +");"
            elif "飙升" in filename:
                sql_insert += "insert into bc_searchwords_risewords " + sql_colunms + ") values" + sql_values +");"
        for sql in sql_list:
            sql_msg = configure.echo(sql)
            conn = pymysql.connect(host=sql_msg["config"]["host"],
                                   port=int(sql_msg["config"]["port"]),
                                   user=sql_msg["config"]["user"],
                                   passwd=sql_msg["config"]["passwd"],
                                   charset=sql_msg["config"]["charset"],
                                   db="baoersqlbasic")
            cursor = conn.cursor()
            try:
                cursor.execute(sql_insert)
                conn.commit()
            except Exception as e:  # 加入异常判定
                conn.rollback()  # 进行回滚
                print(e)
                print(" * SQL进程错误过载，程序保护型中止，请检查错误项目！")
            finally:
                cursor.close()
                conn.close()
        shutil.move(filename, os.path.dirname(filename) + os.path.sep + "searchwords" + os.path.sep + os.path.basename(filename))

if __name__ == "__main__":
    check_date_list(walk_list())
