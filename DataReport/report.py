# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018-06-10 17:59'

import numpy as np
import pandas as pd

from DataReport.config import *

class REPORT_GENERATION(object):
	def __init__(self, df, **kwargs):
		self.df = df
		self.path = kwargs.get("path", default_file_path)
		self.mode = kwargs.get("mode", "vendor_bill")
		self.date = kwargs.get("工作日期：")  # 此处date与tidying中的日期不同
		self.detail = kwargs.get("detail", False)   # 是否显示细节
	
	def run(self):
		datasheet = {
			"financial_store": self.financial_store(),
			"vendor_bill": self.vendor_bill(),
		}
		return datasheet[self.mode]
	
	
	def financial_store(self):
		pass
	
	def vendor_bill(self):
		vendor_list = set(self.df["供应商"])
		result_paper = ''''''
		wrong_reason = {"List": "报货单缺失", "Table": "表格数据缺失", "Number": "条数不符",
		                "Price": "单价不符", "Wrong": "其他错误"}
		self.df["result"] = "Default"
		for vendor in vendor_list:
			df_vendor = self.df.loc[self.df["供应商"]==vendor, :]
			vendor_dict = {"Right":[], "List":[], "Table":[], "Number":[], "Price":[], "Wrong":[]}
			for line in df_vendor.index.tolist():
				if (df_vendor.loc[line, "数量_x"] == df_vendor.loc[line, "数量_y"]) and\
					(df_vendor.loc[line, "单价_x"] == df_vendor.loc[line, "单价_y"]) and\
					(df_vendor.loc[line, "金额_x"] == df_vendor.loc[line, "金额_y"]):
					self.df.loc[line, "result"] = "Right"
					vendor_dict["Right"].append(str(self.df.loc[line, "供应商货号"]))
				elif np.isnan(df_vendor.loc[line, "数量_x"]):
					self.df.loc[line, "result"] = "List"
					vendor_dict["List"].append(str(self.df.loc[line, "供应商货号"]) + "(" + self.df.loc[line, "款式编号"] + ")")
				elif np.isnan(df_vendor.loc[line, "数量_y"]):
					self.df.loc[line, "result"] = "Table"
					vendor_dict["Table"].append(str(self.df.loc[line, "供应商货号"]))
				elif (df_vendor.loc[line, "数量_x"] != df_vendor.loc[line, "数量_y"]) and \
						(df_vendor.loc[line, "单价_x"] == df_vendor.loc[line, "单价_y"]) and \
						(df_vendor.loc[line, "金额_x"] != df_vendor.loc[line, "金额_y"]):
					self.df.loc[line, "result"] = "Number"
					vendor_dict["Number"].append(str(self.df.loc[line, "供应商货号"]))
				elif (df_vendor.loc[line, "数量_x"] == df_vendor.loc[line, "数量_y"]) and \
						(df_vendor.loc[line, "金额_x"] != df_vendor.loc[line, "金额_y"]):
					self.df.loc[line, "result"] = "Price"
					vendor_dict["Price"].append(str(self.df.loc[line, "供应商货号"]))
				else:
					self.df.loc[line, "result"] = "Wrong"
					vendor_dict["Wrong"].append(str(self.df.loc[line, "供应商货号"]))
			# 报表生成
			result_paper += " * 供应商：{} ( 正确条数/总条目数：{} / {} )\n".format(
				vendor, len(vendor_dict["Right"]), len(df_vendor)
			)
			result_paper += " - 错误条目统计：报货单缺失{}条；表数据缺失{}条；条数不符{}条；单价不符{}条；其他错误{}条\n".format(
				len(vendor_dict["List"]), len(vendor_dict["Table"]),
				len(vendor_dict["Number"]), len(vendor_dict["Price"]), len(vendor_dict["Wrong"]),
			)
			for reason in wrong_reason:
				if vendor_dict[reason]:
					result_paper += "   > {} 列表：\n      ".format(wrong_reason[reason])
					for i in vendor_dict[reason]:
						result_paper += i + ", "
					result_paper += "\n"
		return result_paper, self.df
