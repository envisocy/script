#!usr/bin/env python
# -*- coding:utf-8 -*-

import xiaobaods_input
import xiaobaods_input.Business_adviser_parser
import xiaobaods_input.Update_ERP_Sales_Together

try:
    import sys
    argv = sys.argv[1]
    argv = eval(argv)
except:
    argv = 9

if argv == 1:
    xiaobaods_input.run(argv)
elif argv == 8:
    xiaobaods_input.Update_ERP_Sales_Together.run()
elif argv == 9:
    xiaobaods_input.Business_adviser_parser.run()
