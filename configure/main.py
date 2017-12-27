
#!user/bin/env python
# -*- coding: utf-8 -*-
from configure import prpcrypt
import os
from configure.config import *

def _cyclic_reading(dir_path, string=".txt"):
    '''
    循环读取目标文件中包含string字符的文件列表字典
    '''
    l ={}
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            if string in filename:
                l[filename] = dir_path + os.path.sep + filename
    return l

def _return_msg(l):
    '''
    传入文件列表，返回所有的信息，字典形式
    '''
    d = {}
    prp = prpcrypt.prpcrypt()
    for i in l:
        d[i.split(".txt")[0]] = eval(prp.read_file(path="", filename=l[i]))
    return d

def _sql_msg():
    sql_msg={}
    for search_dir in search_dirs:
        dir_list = _cyclic_reading(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + search_dir)
        dir_result = _return_msg(dir_list)
        sql_msg.update(dir_result)
    return sql_msg

if __name__ =='__main__':
    print(_sql_msg())
