# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

from xiaobaods_write import document

def run():
	doc = document.Doc()
	doc.run()
	print(doc.msg)
