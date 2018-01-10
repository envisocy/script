#!usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import sys
    argv = sys.argv[1]
    argv = eval(argv)
except:
    argv = {}

import xiaobaods_output.basic as basic
import xiaobaods_output.reprocessing as reprocessing

fun = argv.get("fun")

if fun in ["pr"]:   # 基于reprocessing所有的fun列表
    program = reprocessing.function(**argv)
    program.run(argv.get("fun", "pr"))
else:
    program = basic.function(**argv)
    program.run(argv.get("fun", "a"))
