#!usr/bin/env python
# -*- coding:utf-8 -*-

def run(operation=1):
    '''
    operation=1:启动关键词处理程式，为今后预留参数
    '''
    if operation==1:
        import xiaobaods_input.keywords as keys
        keys.check_date_list(keys.walk_list())
    print(" ^ 执行完毕！")
