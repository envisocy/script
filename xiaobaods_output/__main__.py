#!usr/bin/env python
# -*- coding:utf-8 -*-

try:
    import sys
    argv = sys.argv[1]
    argv = eval(argv)
except:
    argv = {}

import xiaobaods_output.function as function
basic = function.basic(**argv)
basic.run(argv.get("fun","a"))
