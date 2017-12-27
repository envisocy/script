#!user/bin/env python
# -*- coding: utf-8 -*-

"""
configure
======

管理系统内所有可以连通的数据源的连接信息：

返回的信息格式为：
调用名称：Name：{
    显示别名: 'alias':
    备注信息: 'remark':
    数据源类型: 'style':
    具体参数类型： 'config':{}
    修改时间： 'date':
    }

支持的数据源类型：
数据文件：csv文档
数据库：Mysql
数据库：MongoDB (×)

配置信息目录：
./DatafileConfig/...
> 自动索引该目录列表下所有支持的数据文件配置信息

./DatabaseConfig/...
> 自动索引该目录列表下所有支持的数据库配置信息

"""
from configure import main

def echo(name="localhost"):
    sql_msg = main._sql_msg()
    if name in sql_msg:
        return sql_msg[name]
    else:
        return {'alias': "No such item"}
