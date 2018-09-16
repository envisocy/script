# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

from xiaobaods_write import document
from xiaobaods_write import pattern
from xiaobaods_write import daily

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
	run(mode="doc")