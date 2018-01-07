#!usr/bin/env python3
# -*- coding:utf-8 -*-

import financial_analysis.data_source
import pymysql
from datetime import datetime
import time
import pandas as pd


def write_to_mysql(TableName, dic):
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="financial_statements")
    cursor=conn.cursor()
    COLstr='' # 行字段
    ROWstr='' # 列字段
    for key in dic.keys():
        ColumnStyle=' FLOAT(16,6)'
        if key=="caibaoshuo_url":
            ColumnStyle=' VARCHAR(60)'
        elif key=="code":
            ColumnStyle=' CHAR(10)'
        elif key=="end_month":
            ColumnStyle=' CHAR(2)'
        elif key=="end_year":
            ColumnStyle=' CHAR(4)'
        elif "data" in key:
            ColumnStyle=' INT(8)'
        elif "cash_flow" in key:
            ColumnStyle=' BIGINT(12)'
        COLstr += ' ' + key + ColumnStyle + ','
        ROWstr += ('"%s"'+',')%(dic[key])
    try:
        cursor.execute("SELECT * FROM  %s"%(TableName))
        # Insert
        cursor.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    except Exception as e:
        print(" * 错误：",e)
        try:
            cursor.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
        except:
            print(" * 创建失败")
        # Cteate
        cursor.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    # 记录日志
    try:
        cursor.execute("INSERT INTO record VALUES ('" + str(dic["code"]) + \
                       "','" + str(dic["end_year"]) + "','" + \
                       datetime.strftime(datetime.now(), \
                                         "%Y-%m-%d %H:%M:%S %f") + "');")
    except:
        cursor.execute("UPDATE record SET `time`='" + datetime.strftime(datetime.now(), \
                          "%Y-%m-%d %H:%M:%S %f") + "' WHERE `code`='" + \
                       str(dic["code"]) + "' AND `year`='" + \
                       str(dic["end_year"]) + "';")
    conn.commit()
    cursor.close()
    conn.close()

cbs = financial_analysis.data_source.caibaoshuo()
code_list = cbs.request_list(code="")
for code in code_list:
    data = cbs.get_data(sheets="mj", code=code)
    print(code + " - " + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S %f"))
    for i in data:
        i["code"] = code
        write_to_mysql("mjsheets", i)
    time.sleep(8)
