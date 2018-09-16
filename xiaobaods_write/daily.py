# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/9/4 15:17'

import os
import pandas as pd
import pymysql
import configure
from xiaobaods_write.config import *

class Shop_daily():
	def __init__(self):
		pass
	
	def run(self):
		# 确定路径
		path = self.path()
		print("> Step.2 确认路径 {} ，进行文档检索...".format(path))
		# 检索所有符合条件的文档
		source = self.traversing(path)
		if not source:
			print(" !!! 未找到符合条件的文档：".format(path))
			return None
		print("> Step.3 找到 {} 个文档，开始进行文档处理...".format(len(source)))
		# 遍历文档
		for filename, date in source.items():
			self.handle_file(path, filename, date)
		print("> Step.End 程序处理结束。")

	def path(self):
		print(" > Step.1 请输入文档所在路径...(默认桌面路径{})".format(DESKTOP_DIR))
		path = self.decision_path()
		return path

	def decision_path(self):
		input_path = input(" 直接回车启用桌面路径 : ")
		if input_path == "":
			input_path = DESKTOP_DIR
		if input_path[-1] == os.sep:
			input_path = input_path[:-1]
		if not os.path.exists(input_path):
			print(" !!! 输入的路径不存在！请重新输入合法路径！")
			self.decision_path()
		return input_path
	
	def traversing(self, path):
		source = {}
		file_list = os.listdir(path)
		for file in file_list:
			if ("【生意参谋】商品效果" in file) and (file[-3:] == "xls") and (len(file) > 35):
				if file[11:21] == file[22:32]:
					source.update({file:file[11:21]})
				else:
					print(" !!! {} 导出非一天数据！".format(file))
		return source
	
	def handle_file(self, path, filename, date):
		df = pd.read_excel(path + os.sep + filename, header=3, )
		# 百分号处理
		for column in PERCENT_TRANSFORM:
			df[column] = df[column].str.strip("%").astype(float)/100
		# 判断终端
		if df.loc[1, "所属终端"] != "所有终端":
			print(" !!! 终端选择错误！")
			return None
		# 品牌判断
		brand_list_raw = self.sql_answer(sql="xiaobaods_w", sql_centence="SELECT abbreviation FROM `shops.query`;",
		                                 db="baoersqlerp")
		brand_list = [item[0] for item in brand_list_raw]
		brand = self.title_test(df.loc[:, "商品标题"].tolist(), brand_list)
		# 更换标题
		df["date"] = date
		df["brand"] = brand
		df.rename(columns = COLUMNS_SWITCH, inplace=True)
		df.drop("商品链接", axis=1, inplace=True)
		# 写入数据
		centence = ""
		data_num = 0
		for index in range(len(df)):
			key_centence = ""
			value_centence = ""
			line = df.iloc[index, :]
			for key in line.keys():
				key_centence += "`" + str(key) + "`" + ","
			for value in line:
				value_centence += "'" + str(value) + "'" + ","
			centence += "INSERT INTO `{}`({}) VALUES({});".format("store_daily_data", key_centence[:-1], value_centence[:-1])
			data_num += 1
		data = self.sql_answer("xiaobaods_w", centence)
		print("{} {}({})".format(filename, data, data_num))
		
	def sql_answer(self, sql, sql_centence, db="baoersqlos"):
		data = ""
		conn = pymysql.connect(
			host=configure.echo(sql)["config"]["host"],
			port=configure.echo(sql)["config"]["port"],
			user=configure.echo(sql)["config"]["user"],
			passwd=configure.echo(sql)["config"]["passwd"],
			charset=configure.echo(sql)["config"]["charset"],
			db=db)
		try:
			cursor = conn.cursor()
			cursor.execute(sql_centence)
			conn.commit()
			data = cursor.fetchall()
			if not data:
				data = "写入完毕"    # 返回一个标记
		except Exception as e:
			conn.rollback()
			data = str(e)
		finally:
			cursor.close()
			conn.close()
		return data
	
	def title_test(self, title_list, brand_list):
		brand_win = ""
		brand_rank = 0
		for brand in brand_list:
			rank = 0
			for title in title_list:
				if brand in title:
					rank += 1
			if rank > brand_rank:
				brand_win = brand
				brand_rank = rank
		if brand_rank > 2:
			return brand_win
		else:
			return input(" 无法确定品牌，请输入：")
