# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/11 10:35'

# 命令行运行

from xiaobaods_write import document

def run():
	doc_instance = document.Doc()
	doc_instance.run()
	if doc_instance.error:
		print(doc_instance.error)

if __name__ == "__main__":
	run()
