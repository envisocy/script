#!usr/bin/env python
# -*- coding:utf-8 -*-


def sql_msg():
    sql_msg ={}
    with open("sql_msg.txt") as f:
        line = f.readline()
        while line:
            sql_msg[line.split("=")[0]] = line.split("=")[1].split(u"\n")[0]
            line = f.readline()
    try:
        sql_msg["port"] = int(sql_msg["port"])
    finally:
        pass
    return sql_msg


class sqlserver():
    import pymsql
    def __init__(self):
        self.sql_msg = sql_msg()

    def call_sql(self, sentence):
        conn = pymysql.connect(host=self.sql_msg["host"], port=self.sql_msg["port"],
                               user=self.sql_msg["user"], passwd=self.sql_msg["passwd"],
                               charset=self.sql_msg["charset"], db=self.sql_msg["db"])
        cursor = conn.cursor(sentence)
        rs = cursor.fetchall()
        cursor.close()
        conn.close()
        return rs
        

a = sqlserver()
a.msg()
