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
elif argv == 90:
    import xiaobaods_output.reprocessing as rep
    func = rep.function()
    func.pr_input()
elif argv // 10 == 9 and argv % 10 < 10:
    import datetime
    import xiaobaods_output.reprocessing as rep
    func = rep.function()
    func.pr_input(date=datetime.datetime.strftime(
        datetime.datetime.now().date() -datetime.timedelta(argv % 10 + 1),
        "%Y-%m-%d"))
