# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018-06-10 10:30'

import os
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.parser import parse

from DataReport.config import *


class FILE_TIDYING(object):
	# 通过字典返回要外部提示的内容
	# self.mode参数控制self.run()函数的具体运行
	def __init__(self, **kwargs):
		self.mode = kwargs.get("mode", "vendor_bill")
		self.date = kwargs.get("date", "")
		self.path = kwargs.get("path", default_file_path)
		if self.date:
			self.date = parse(self.date)
	
	def run(self):
		datasheet = {
			"financial_store": self.financial_store(),
			"vendor_bill": self.vendor_bill(),
		}
		return datasheet[self.mode]
	
	def financial_store(self):
		pass
	
	def vendor_bill(self):
		path = self.path + os.sep + default_vendor_bill_folder
		# 若self.date存在，则路径更改为默认名+日期
		if self.date:
			path += datetime.strftime(self.date, "%Y-%m-%d")
		list_dir = os.listdir(path)
		# 查找采购入库文件
		find_inspect = 0
		for i in list_dir:
			if "采购入库" in i:
				# 从采购入库文件中拿到供应商列表
				df = pd.read_excel(os.path.join(path, i))
				df.loc[:, "供应商"].dropna(inplace=True)
				PW_vendor_list = list(set(df.loc[:, "供应商"]))
				for item in PW_vendor_list:
					if item not in vendor_message:
						PW_vendor_list.remove(item)     # 与档口的总列表比对
				PW_date = datetime.strptime(df.loc[6, "单据日期"].split()[0], "%Y/%m/%d")
				# 如果self.date不为空，则添加验证时间步骤
				if self.date:
					if self.date != PW_date:
						print(" * 文件夹名时间与入库时间不符！( {} vs {} )".format(self.date, PW_date))
						return None
				else:
					self.date = PW_date
				# ---
				PurchasingWarehousing = "采购入库"  + datetime.strftime(PW_date, "%Y-%m-%d") + "." + i.split(".")[-1]
				os.rename(os.path.join(path, i), os.path.join(path, PurchasingWarehousing))
				list_dir.remove(i)
				find_inspect += 1
		if find_inspect == 0:
			print(" * 未找到采购入库文件，请检查文件夹文件！")
			return None
		elif find_inspect > 1:
			print(" * 采购入库文件过多，请检查文件夹文件！")
			return None
		# 查找供应商文件并改名
		file_list = {}
		PW_vendor_list_tidy = []   # 处理过的文件列表
		PW_vendor_list_remain = PW_vendor_list.copy()   # 采购入库有，而供应商未发文件
		PW_vendor_list_miss = []    # 供应商发文件，而采购入库没有
		for filename in list_dir:
			for vendorname in vendor_message:
				# filename:xxx.xlsx; vendorname:xxx 如果符合筛选条件：
				if (vendor_message[vendorname]["include"] in filename) and \
						(vendor_message[vendorname].get("except", "^") not in filename):
					# 针对文件名包含时间的解析，只判断供应商后，扩展名前的部分是否可以解析为时间
					try:
						filename_date = parse(filename.split(vendorname)[-1].split(".")[0])
						if filename_date == PW_date:
							pass
						else:
							print(" * 采购入库时间与[{}]文件名时间不一致".format(vendorname))
					except:
						pass
					finally:
						new_name = os.path.join(path,
						        vendorname + datetime.strftime(PW_date, "%Y-%m-%d") + "." + filename.split(".")[-1])
						os.rename(os.path.join(path, filename), new_name)
						find_inspect += 1
						PW_vendor_list_tidy.append(vendorname)
						file_list.update({new_name: vendorname})
					if vendorname in PW_vendor_list_remain:
						PW_vendor_list_remain.remove(vendorname)
					elif vendorname not in PW_vendor_list:
						PW_vendor_list_miss.append(vendorname)
		return {"工作日期：": datetime.strftime(self.date, "%Y-%m-%d"), "文件列表：": file_list,
		        "处理数量：": find_inspect-1, "处理文件：": PW_vendor_list_tidy, "文件缺失：": PW_vendor_list_remain,
		        "文件溢出：": PW_vendor_list_miss, }
	





