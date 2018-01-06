#!usr/bin/env python3
# -*- coding:utf-8 -*-

import financial_analysis.data_source.caibaoshuo
import pymysql
from datetime import datetime
import time


def write_to_mysql(TableName, dic):
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="financial_statements")
    cursor=conn.cursor()
    COLstr='' # 行字段
    ROWstr='' # 列字段
    for key in dic.keys():
        ColumnStyle=' FLOAT(10,6)'
        if key=="caibaoshuo_url":
            ColumnStyle=' VARCHAR(60)'
        elif key=="code":
            ColumnStyle=' CHAR(10)'
        elif key=="end_month":
            ColumnStyle=' CHAR(2)'
        elif key=="end_year":
            ColumnStyle=' CHAR(4)'
        COLstr += ' ' + key + ColumnStyle + ','
        ROWstr += ('"%s"'+',')%(dic[key])
    try:
        cursor.execute("SELECT * FROM  %s"%(TableName))
        # Insert
        cursor.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    except:
        cursor.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
        # Cteate
        cursor.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    try:
        cursor.execute("INSERT INTO record VALUES ('" + str(dic["code"]) + "','" + str(dic["end_year"]) + "','" + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S %f") + "');")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

cbs = caibaoshuo()
code_list = cbs.request_list(code="")
for code in code_list:
    data = cbs.get_data(sheets="oj", code=code)
    print(code)
    for i in data:
        i["code"] = code
        write_to_mysql("mjsheets", i)
    time.sleep(8)
