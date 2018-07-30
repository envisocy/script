# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/25 13:52'

# 固定格式化内容的数据收集

import sys
import pandas as pd
import shutil
import pymysql
import os

from xiaobaods_write.config import *

class Pat():
	def __init__(self):
		self.dir = self.find_dir()
		self.msg = " *** 生意参谋关键词录入模块 ***\n * From: {}{}\n" \
		           " * A new processing engine: Ailurus fulgens X\n *** *** *** *** *** *** ***\n".format(
			self.dir, os.sep)
		
		
	def run(self):
		print(self.msg)
		self.check_date_list(self.return_date_list())
		print("* 运行完毕，所有完整的文档已经完成录入！")
	
	def find_dir(self):
		if "win" in sys.platform:
			top_list = TOP_LIST_WIN
		elif "linux" in sys.platform:
			top_list = TOP_LIST_LINUX
		else:
			top_list = []
		return top_list
		
	def return_date_list(self):
		date_list = {}
		for floder in self.dir:
			try:
				for filename in os.listdir(floder):
					if "生意参谋" in filename:
						if filename[8:18] not in date_list:
							date_list[filename[8:18]] = set()
						date_list[filename[8:18]].add(floder + os.path.sep + filename)
			except:
				pass
		return date_list

	def check_date_list(self, date_list):
		for date_set in date_list:
			if len(date_list[date_set]) == 30:
				print(" * 处理", date_set, "中...")
				self.write_to_sql(date_list[date_set])
				print(" * 处理", date_set, "完毕!")
			else:
				print(" # ", date_set, "文档缺失，请确认后重新处理！")

	def write_to_sql(self, filenames, sql_list=SQL_LIST_PATTERN):
		import configure
		for filename in filenames:
			sql_insert = ""
			df= pd.read_excel(filename, header=3)
			print(filename)
			for r in range(len(df)):
				basename = os.path.basename(filename)
				sql_colunms ="(日期,类目,渠道,字段,"
				sql_values ="('"+basename[8:18]+"','"+basename[29:32]+"','"+basename[39:43]+"','"+basename[33:38]+"',"
				for s in df.columns:
					if s != df.columns[-1]:
						if s == "词均支付转化率":
							sql_colunms += "支付转化率,"
							sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
						elif s == "词均点击率":
							sql_colunms += "点击率,"
							sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
						else:
							sql_colunms += str(s)+","
							sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"',"
					else:
						sql_colunms += str(s)
						sql_values += "'"+str(df.loc[r,s]).replace("'","`")+"'"
				if "热搜" in filename:
					sql_insert += "insert into bc_searchwords_hotwords " + sql_colunms + ") values" + sql_values +");"
				elif "飙升" in filename:
					sql_insert += "insert into bc_searchwords_risewords " + sql_colunms + ") values" + sql_values +");"
			for sql in sql_list:
				sql_msg = configure.echo(sql)
				conn = pymysql.connect(host=sql_msg["config"]["host"],
									   port=int(sql_msg["config"]["port"]),
									   user=sql_msg["config"]["user"],
									   passwd=sql_msg["config"]["passwd"],
									   charset=sql_msg["config"]["charset"],
									   db="baoersqlbs")
				cursor = conn.cursor()
				try:
					cursor.execute(sql_insert)
					conn.commit()
					print(" * 写入 {} 成功！".format(sql))
				except Exception as e:  # 加入异常判定
					conn.rollback()  # 进行回滚
					print(" * 写入 {} 错误：{}".format(sql, e))
				finally:
					cursor.close()
					conn.close()
			shutil.move(filename, os.path.dirname(filename) + os.path.sep + "searchwords" + os.path.sep + os.path.basename(filename))
