#!usr/bin/env python
# -*- coding: utf-8 -*-


import pymysql
import hashlib
from xiaobaods_input.Business_adviser_parser.config import *
from pyquery import PyQuery as pq
import configure


def detector_main_control(mode, table, sql_list=["localhost"], date=""):
    if mode == 4:
        detector_mode4(date, table, sql_list)


def detector_mode1():
    pass


def detector_mode2():
    pass


def detector_mode4(date, table, sql_list):
    for sql in sql_list:
        for category in MODE4_PERMIT:
            print("#" * 70)
            print(" 日期：", date, "\t\t类目：", category, "\t\t终端：", sql)
            print("#" * 70)
            for attribute, form in MODE4_PERMIT[category].items():
                sql_select = "SELECT max(热销排名),count(*) from "+table+" WHERE 类目='"+category+"' " \
                             "AND 类型='"+form+"' AND 属性='"+attribute+"' AND 日期='"+date+"' GROUP BY 类目,类型,属性,日期;"
                conn = pymysql.connect(
                    host=configure.echo(sql)["config"]["host"],
                    port=configure.echo(sql)["config"]["port"],
                    user=configure.echo(sql)["config"]["user"],
                    passwd=configure.echo(sql)["config"]["passwd"],
                    charset=configure.echo(sql)["config"]["charset"],
                    db="baoersqlbasic")
                try:
                    cursor = conn.cursor()
                    cursor.execute(sql_select)
                    result = cursor.fetchall()
                    print("类型：", form, "\t属性：", attribute, "\t\t最大：", result[0][0], " \t条目数：", result[0][1])
                except:
                    print("类型：", form, "\t属性：", attribute, "\t\t最大：- \t\t条目数： -")
                finally:
                    cursor.close()
                    conn.close()
