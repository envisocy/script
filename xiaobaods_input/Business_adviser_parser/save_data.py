#!usr/bin/env python
# -*- coding: utf-8 -*-


import pymysql
from xiaobaods_input.Business_adviser_parser.config import *
import configure


def validation_exists2(id, date, sql_list=["localhost"]):
    sql = sql_list[-1]
    conn = pymysql.connect(
            host=configure.echo(sql)["config"]["host"],
            port=configure.echo(sql)["config"]["port"],
            user=configure.echo(sql)["config"]["user"],
            passwd=configure.echo(sql)["config"]["passwd"],
            charset=configure.echo(sql)["config"]["charset"],
            db="baoersqlbasic")
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM bc_commodity_items WHERE `日期`='" + date + "' and `id`='" + id + "';")
    conn.commit()
    cursor.close()
    conn.close()
    if result:
        print("* 忽略：该条信息已经存在！")
        return 1

def save_main_control(mode, msg, items, sql_list=["localhost"], type="mysql", table=""):
    if mode == 1 and type == "mysql":
        return save_to_mysql_mode1(mode, msg, items, sql_list)
    if mode == 2 and type == "mysql":
        return save_to_mysql_mode2(msg, items, table, sql_list)
    if mode == 3 and type == "mysql":
        return save_to_mysql_mode1(mode, msg, items, sql_list)  # ues mode1
    if mode == 4 and type == "mysql":
        return save_to_mysql_mode1(mode, msg, items, sql_list)
    return None


def save_to_mysql_mode1(mode, msg, items, sql_list=["localhost"]):
    sql_insert = ""
    if mode == 1 or mode == 3:
        sql_insert = ""
        table1 = {1: "brand", 3: "attribute"}
        table2 = {"热销商品榜": "sales", "流量商品榜": "visitor"}
        table = "bc_{0}_granularity_{1}".format(
            table1[mode], table2[msg.get('head')])
    elif mode == 4:
        table = "bc_category_granularity"
    for item in items:
        sql_value = ""
        sql_columns = str(tuple(item.keys())).replace("'", "`")
        for i in item:
            sql_value += "'" + item[i] + "',"
        sql_values = "(" + sql_value[:-1] + ")"
        sql_insert += "INSERT INTO " + table + \
            sql_columns + " VALUES " + sql_values + ";"
    for sql in sql_list:
        conn = pymysql.connect(
            host=configure.echo(sql)["config"]["host"],
            port=configure.echo(sql)["config"]["port"],
            user=configure.echo(sql)["config"]["user"],
            passwd=configure.echo(sql)["config"]["passwd"],
            charset=configure.echo(sql)["config"]["charset"],
            db="baoersqlbasic")
        try:
            cursor = conn.cursor()
            cursor.execute(sql_insert)
            conn.commit()
            print("# ", sql, ":Write successfully")
        except Exception as e:
            prompt_message(mode=1, msg=msg, detail=1)
            print("* 错误：", e)
        finally:
            cursor.close()
            conn.close()
    return table


def save_to_mysql_mode2(msg, items, table, sql_list=["localhost"]):
    sql_insert = ""
    for item in items:
        sql_value = ""
        sql_columns = str(tuple(item.keys())).replace("'", "`")
        for i in item:
            sql_value += "'" + item[i] + "',"
        sql_values = "(" + sql_value[:-1] + ")"
        sql_insert += "INSERT INTO " + table + sql_columns + " VALUES " + sql_values + ";"
    for sql in sql_list:
        conn = pymysql.connect(
            host=configure.echo(sql)["config"]["host"],
            port=configure.echo(sql)["config"]["port"],
            user=configure.echo(sql)["config"]["user"],
            passwd=configure.echo(sql)["config"]["passwd"],
            charset=configure.echo(sql)["config"]["charset"],
            db="baoersqlbasic")
        try:
            cursor = conn.cursor()
            cursor.execute(sql_insert)
            conn.commit()
        except pymysql.err.InternalError as e:
            pass
        except pymysql.err.IntegrityError as e:
            code, message = e.args
            print("* 错误：", message[-17:])
        except Exception as e:
            prompt_message(mode=2, msg=msg, detail=1)
            print("* 错误：", e)
            print(type(e))
        finally:
            cursor.close()
            conn.close()
    return table


def prompt_message(mode, msg, detail=0):
    if mode == 1:
        if detail == 0:
            print("- 〔", msg.get('head'), "〕日期：", msg.get('brand'), "@", msg.get('main'), " Page: ", msg.get("curr"), "/", msg.get("total"))
        elif detail == 1:
            print("- 目录：【", msg.get('mask'), "-", msg.get('header'), "】")
            print("- 参数：〖", msg.get('main'), "/", msg.get('category'), "/", msg.get('brand'), "/", msg.get('device'), "/", \
                  msg.get('seller'), "〗")
            print("- 细节：〔", msg.get('head'), "〕 Max items: ", msg.get('quantity'), " Page: ", msg.get("curr"), "/", \
                  msg.get("total"))
    elif mode == 2:
        if detail == 0:
            print("- 〔", msg.get('id'), "〕品牌：", msg.get('brand'), " 日期：", msg.get('main'))
        elif detail == 1:
            print("- 目录：【", msg.get('mask'), "-", msg.get('header'), "】")
            print("- 参数：〖", msg.get('main'), "@", msg.get('title'), "〗")
            print("- 商品ID：〔", msg.get('id'), "〕", msg.get('shopname'), ": ", msg.get("brand"))
    elif mode == 3:
        if detail == 0:
            print("- 〔", msg.get('head'), "〕类目：", msg.get('category'), "@", msg.get('main'), " Page: ", msg.get("curr"), "/", msg.get("total"))
        elif detail == 1:
            print("- 目录：【", msg.get('mask'), "-", msg.get('header'), "】")
            print("- 参数：〖", msg.get('main'), "/", msg.get('category'), "/", msg.get('brand'), "/", msg.get('device'), "/", \
                  msg.get('seller'), "〗")
            print("- 细节：〔", msg.get('head'), "〕 Max items: ", msg.get('quantity'), " Page: ", msg.get("curr"), "/", \
                  msg.get("total"))
    elif mode == 4:
        if detail == 0:
            print("- 〔", msg.get('head'), "〕类目：", msg.get('category'), "-", msg.get('attribute'), "@", msg.get('main'), " Page: ", msg.get("curr"), "/", msg.get("total"))
        elif detail == 1:
            print("- 目录：【", msg.get('mask'), "-", msg.get('header'), "】")
            print("- 参数：〖", msg.get('main'), "/", msg.get('category'), "/", msg.get('attribute'), "/", msg.get('device'), "/", \
                  msg.get('seller'), "〗")
            print("- 细节：〔", msg.get('head'), "〕 Max items: ", msg.get('quantity'), " Page: ", msg.get("curr"), "/", \
                  msg.get("total"))
    return None
