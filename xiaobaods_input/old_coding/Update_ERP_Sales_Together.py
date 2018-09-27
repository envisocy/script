#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configure
import datetime
import pymysql


def date_crange(date_min, date_max):
    date = date_max
    date_range_list = []
    while date != date_min:
        date_range_list.append(date)
        date -= datetime.timedelta(1)
    return date_range_list

def operation_pymysql(SQL_select="", SQL="xiaobaods_w"):
    SQL_msg=configure.echo(SQL)["config"]
    conn = pymysql.connect(host=SQL_msg["host"], port=int(SQL_msg["port"]),
                           user=SQL_msg["user"], passwd=SQL_msg["passwd"],
                           charset=SQL_msg["charset"], db="baoersqlerp")
    cursor = conn.cursor()
    cursor.execute(SQL_select)
    conn.commit()
    return_variable = cursor.fetchall()
    cursor.close()
    conn.close()
    return return_variable

def run():
    time_s = datetime.datetime.now()
    print(" *** Script For ERP_Sales_ledger Updating ERP_Sales_Together ***\n"+\
          " *** Ver_04 # 12-30-2017 @ Compliance with the GPL agreement ***")
    # 查找Sales_ledger中的时间范围
    date_range = operation_pymysql("SELECT max(`交易时间`),min(`交易时间`) FROM ERP_Sales_Ledger;")[0]
    print(" *** Dynamic update range: %s - %s (Reverse) ***\n" % \
          (datetime.datetime.strftime(date_range[1].date(), "%Y-%m-%d"), \
           datetime.datetime.strftime(date_range[0].date(), "%Y-%m-%d")))
    date_range_list = date_crange(date_range[1].date(), date_range[0].date())
    # 倒序进行生成操作
    print(" - Prepare and Connect database...\n")
    for date in date_range_list:
        # 判断是否需要更新
        print(" - [" + str(datetime.datetime.now() - time_s)[:12] + "] * " \
              + datetime.datetime.strftime(date, "%Y-%m-%d") + " *: ",end="")
        total_ledger = operation_pymysql("SELECT sum(`数量`) FROM \
            ERP_Sales_Ledger WHERE `交易时间` like '" + \
            datetime.datetime.strftime(date,"%Y-%m-%d") + "%' AND \
            `仓库`<>'虚拟仓库' AND `货品编号`<>'A';")[0][0]
        total_together = operation_pymysql("SELECT sum(`件数`) FROM \
            ERP_Sales_Together WHERE `交易时间` like '" + \
            datetime.datetime.strftime(date,"%Y-%m-%d") + "%';")[0][0]
        # 更新操作
        if total_ledger != total_together:
            print("Dynamic updating... (" + str(total_ledger) + " -> " + \
                  str(total_together) + ")")
            operation_pymysql("DELETE FROM ERP_Sales_Together WHERE `交易时间`=\
                    '" + datetime.datetime.strftime(date, "%Y-%m-%d") +"';")
            operation_pymysql("INSERT INTO ERP_Sales_Together SELECT '" + \
                datetime.datetime.strftime(date,"%Y-%m-%d") + "',E.`店铺`, \
                I.`operator` as 组长,I.`team` as 项目组, sum(E.合计) - \
                sum(E.分摊优惠) + sum(E.应收邮资) as 销售额, sum(`数量`) as 总件数, \
                POW(sum(E.合计) - sum(E.分摊优惠) + sum(E.应收邮资), 1/1.6) as 销售指数, \
                POW(sum(`数量`), 1/1.4) as 件数指数 FROM inside_stores AS I, ERP_Sales_Ledger AS E \
                WHERE I.`STORE`=E.`店铺` AND E.`交易时间` like '" + \
                datetime.datetime.strftime(date,"%Y-%m-%d") + "%' and \
                E.`货品编号`<>'A' and E.`仓库`<>'虚拟仓库' GROUP BY E.`店铺`;")
        else:
            print("Ignore and Skip updates...")
