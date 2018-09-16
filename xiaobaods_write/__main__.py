# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

# 命令行运行

from xiaobaods_write import document
from xiaobaods_write import pattern
from xiaobaods_write import daily


try:
	import sys
	argv = sys.argv[1]
	argv = eval(argv)
except:
	argv = 9


def run(mode="doc"):
	if mode == "pat":
		pat_instance = pattern.Pat()
		pat_instance.run()
	elif mode == "doc":
		doc_instance = document.Doc()
		doc_instance.run()
		if doc_instance.error:
			print(doc_instance.error)
	elif mode == "sd":
		shop_daily = daily.Shop_daily()
		shop_daily.run()

if __name__ == "__main__":
	if argv == 1:
		argv_mode="pat"
	elif argv == 2:
		argv_mode="sd"
	elif argv == 9:
		argv_mode="doc"
	run(mode=argv_mode)
