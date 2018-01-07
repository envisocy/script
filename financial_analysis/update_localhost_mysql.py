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
                       "','" + str(dic["end_year"]) + "','" + now_time() + "');")
    except:
        cursor.execute("UPDATE record SET `time`='" + now_time() + "' WHERE `code`='" + \
                       str(dic["code"]) + "' AND `year`='" + \
                       str(dic["end_year"]) + "';")
    conn.commit()
    cursor.close()
    conn.close()

def return_exist_list():
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="financial_statements")
    cursor=conn.cursor()
    cursor.execute("SELECT DISTINCT(`code`) FROM record;")
    exist_code_list = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    exist_code_list = [i[0] for i in exist_code_list]
    return exist_code_list

def now_time():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S %f")

print(" - [" + now_time() + "] 程序开始，初始化中...")
cbs = financial_analysis.data_source.caibaoshuo()
print(" - [" + now_time() + "] 初始化完毕，读取总列表中...")
code_list = cbs.request_list(code="")
print(" - [" + now_time() + "] Total: " + str(len(code_list)))
exist_code_list = return_exist_list()
print(" - [" + now_time() + "] Exist: " + str(len(exist_code_list)))
for i in exist_code_list:
    code_list.remove(i)
print(" - [" + now_time() + "] Remaining: " + str(len(code_list)))
for code in code_list:
    data = cbs.get_data(sheets="mj", code=code)
    if not data: # 银行，券商等
        print(" * [" + now_time() + "] 忽略：" + code + "中...")
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="financial_statements")
            cursor=conn.cursor()
            cursor.execute("INSERT INTO record VALUES ('" + str(code) + "','2000','" + now_time() + "');")
            conn.commit()
            cursor.close()
            conn.close()
        except:
            print(" * [" + now_time() + "] 写入忽略列表失败！")
        continue
    elif data=="Timeout":
        print(" - [" + now_time() + "] 连接超时，跳过处理：" + code + "中...")
        continue
    else:
        print(" - [" + now_time() + "] 处理：" + code + "中...")
    for i in data:
        i["code"] = code
        write_to_mysql("mjsheets", i)
    time.sleep(8)
