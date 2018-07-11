# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018-06-10 17:58'

import pandas as pd

from DataReport.config import *


class FORMATTED_DATA(object):
	def __init__(self, **kwargs):
		self.path = kwargs.get("path", default_file_path)
		self.mode = kwargs.get("mode", "vendor_bill")
		self.date = kwargs.get("工作日期：")  # 此处date与tidying中的日期不同
		self.file_list = kwargs.get("文件列表：", "")    # 字典形式{供应商文件: 供应商名}
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
		dfr = pd.DataFrame()
		# 文件信息汇总
		for file, vendor in self.file_list.items():
			print(vendor)
			df = pd.read_excel(file, index_col=None, header=None)
			print(vendor, ": ", len(df))
			format = FORMAT_VENDOR(df, vendor, self.date)
			df0, msg = format.run()
			df0["供应商"] = vendor
			dfr = pd.concat([dfr, df0], axis=0)
		dfr["供应商货号"] = dfr["供应商货号"].astype("str")
		dfr["供应商货号"] = dfr["供应商货号"].map(lambda s:s.split(".")[0])       # 调整为去零的标准格式
		# 资料汇总
		dfc = pd.read_excel(self.path + os.sep + "供应商账单" + self.date + os.sep + "采购入库" + self.date + ".xlsx")
		dfc["供应商货号"] = dfc["供应商货号"].astype("str")
		dfs = dfc.loc[:, ["供应商", "款式编号", "供应商货号", "数量", "金额"]]
		dfs_price = dfc.loc[:, ["供应商", "款式编号", "供应商货号", "单价"]]
		dfs = dfs.groupby(["供应商", "款式编号", "供应商货号"], as_index=False).sum()
		dfs_price = dfs_price.groupby(["供应商", "款式编号", "供应商货号"], as_index=False).mean()
		dfs = pd.merge(dfs, dfs_price, on=["供应商", "款式编号", "供应商货号"])
		# 表单合并
		df = pd.merge(dfr, dfs, how="outer", on=["供应商", "供应商货号"])
		return df

class FORMAT_VENDOR():
	def __init__(self, df, vendor, date):
		self.df = df
		self.vendor = vendor
		self.date = date
		self.num_list = [(i+1)/10 for i in range(100000)]
		
	def run(self):
		if vendor_message[self.vendor].get("format", 0)==0:
			return self.blank()
		elif vendor_message[self.vendor].get("format", 0)==1:
			return self.xml()
		elif vendor_message[self.vendor].get("format", 0)==2:
			return self.bfb(remark=10)
		elif vendor_message[self.vendor].get("format", 0)==2.1:
			return self.bfb(remark=11)
		elif vendor_message[self.vendor].get("format", 0)==3:
			return self.chg()
		elif vendor_message[self.vendor].get("format", 0)==4:
			return self.gdx()
		elif vendor_message[self.vendor].get("format", 0)==5:
			return self.mcs(header=0)
		elif vendor_message[self.vendor].get("format", 0)==5.1:
			return self.mcs(header=1)
		elif vendor_message[self.vendor].get("format", 0)==5.2:
			return self.mcs(sub=1)
		elif vendor_message[self.vendor].get("format", 0)==6:
			return self.mgs()
		elif vendor_message[self.vendor].get("format", 0)==7:
			return self.mlk()
		elif vendor_message[self.vendor].get("format", 0)==8:
			return self.xim()
		elif vendor_message[self.vendor].get("format", 0)==9:
			return self.xis()
		elif vendor_message[self.vendor].get("format", 0)==10:
			return self.chu()
	
	def blank(self):
		df0 = pd.DataFrame()
		return df0, None
	
	@classmethod
	def groupbyagg(cls, df0):
		# "供应商货号", "数量", "单价", "金额", "备注"
		df0["供应商货号"] = df0["供应商货号"].astype("str")
		df0["数量"] = df0["数量"].astype("int")
		df0["单价"] = df0["单价"].astype("float")
		df0["金额"] = df0["金额"].astype("float")
		df0["备注"] = df0["备注"].astype("str")
		df1 = df0.loc[:, ["供应商货号", "数量", "金额", "备注"]]
		df2 = df0.loc[:, ["供应商货号", "单价"]]
		df3 = df0.loc[:, ["供应商货号", "备注"]]
		df1 = df1.groupby("供应商货号", as_index=False).sum()
		df2 = df2.groupby("供应商货号", as_index=False).mean()
		df3 = df3.groupby("供应商货号", as_index=False).sum()
		df0 = pd.merge(df1, df2, on="供应商货号")
		df0 = pd.merge(df0, df3, on="供应商货号")
		print(df0)
		return df0
		
	
	def xml(self):
		# No.1 阿海 xxx销售单
		df0 = self.df
		df0 = df0[df0.iloc[:, 15].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 16].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 17].isin(self.num_list)]
		df1 = None
		# ---
		df0 = df0.iloc[:, [1, 15, 16, 17, 18]]
		df0[18] = df0[18].fillna("-")
		df0.rename(columns={1: "供应商货号", 15: "数量", 16: "单价", 17: "金额", 18: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def bfb(self, remark=10):
		# No.2 百分百、莎莎、沙狼豹 票证日期 增加金额 减少金额
		df0 = self.df[self.df.iloc[:, 5].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 6].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 7].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [2, 5, 6, 7, remark]]
		df0[remark] = df0[remark].fillna("-")
		df0.rename(columns={2: "供应商货号", 5: "数量", 6: "单价", 7: "金额", remark: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
		
	def chg(self):
		# No.3 自制表格 创辉工厂
		df0 = self.df[self.df.iloc[:, 10].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 11].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 12].isin(self.num_list)]
		# --- 16 返货日期
		df0 = df0.loc[:, [1, 10, 11, 12, 17]]
		df0[17] = df0[17].fillna("-")
		df0.rename(columns={1: "供应商货号", 10: "数量", 11: "单价", 12: "金额", 17: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def gdx(self):
		# No.4 古德 xxx销售单<>
		df0 = self.df[self.df.loc[:, 12].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 13].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 14].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [0, 12, 13, 14, 17]]
		df0[17] = df0[17].fillna("-")
		df0.rename(columns={0: "供应商货号", 12: "数量", 13: "单价", 14: "金额", 17: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def mcs(self, header=0, sub=0):
		# No.5 迈纯,西部牛仔 销售单 无尺码分类
		df0 = self.df[self.df.loc[:, 3-sub].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 4-sub].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 5-sub].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [header, 3-sub, 4-sub, 5-sub, 6-sub]]
		# import re       # 因为编码与颜色混合，故需将颜色分离
		# for line in range(len(df0)):
		# 	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		# 	match = zhPattern.search(str(df0.iloc[line, header]))
		# 	if match:
		# 		df0.iloc[line, header] = str(df0.iloc[line, header])[:-1]
		# 	else:
		# 		df0.iloc[line, header] = str(df0.iloc[line, header])
		df0[6-sub] = df0[6-sub].fillna("-")
		df0.rename(columns={header: "供应商货号", 3-sub: "数量", 4-sub: "单价", 5-sub: "金额", 6-sub: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg

	def mgs(self):
		# No.6 玫瑰 自制表格
		num_list = [str(i) for i in self.num_list]
		num_list_d = [str(i+1)+".00" for i in range(1000)]
		df0 = self.df[self.df.loc[:, 15].isin(num_list)]
		df0 = df0[df0.iloc[:, 16].isin(num_list_d)]
		# ---
		df0 = df0.loc[:, [3, 15, 16, 17, 18]]
		df0[15] = df0[15].astype('int')
		df0[16] = df0[16].astype('float64')
		df0[17] = df0[17].astype('float64')
		df0[18] = df0[18].fillna("-")
		df0[18] = df0[18].astype('str')
		df0.rename(columns={3: "供应商货号", 15: "数量", 16: "单价", 17: "金额", 18: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def mlk(self):
		# No.7 米拉卡 自制表格
		self.df[0] = self.df[0].fillna(method="ffill")  # 解决日期不全的问题
		for i in range(len(self.df)):
			self.df.iloc[i, 0] = str(self.df.iloc[i, 0]).split()[0]
		self.df = self.df.loc[self.df[0] == self.date, :]
		df0 = self.df[self.df.loc[:, 11].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 12].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 13].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [2, 11, 12, 13, 17]]
		df0[17] = df0[17].fillna("-")
		df0.rename(columns={2: "供应商货号", 11: "数量", 12: "单价", 13: "金额", 17: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def xim(self):
		# No.8 小美 应收款明细报表
		df0 = self.df[self.df.loc[:, 12].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 13].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 14].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [6, 12, 13, 14, 19]]
		df0[19] = df0[19].fillna("-")
		df0.rename(columns={6: "供应商货号", 12: "数量", 13: "单价", 14: "金额", 19: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def xis(self):
		# No.9 小宋 自制表格
		df0 = self.df[self.df.loc[:, 3].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 4].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 5].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [2, 3, 4, 5, 8]]
		df0[8] = df0[8].fillna("-")
		df0.rename(columns={2: "供应商货号", 3: "数量", 4: "单价", 5: "金额", 8: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
	
	def chu(self):
		# No.10 创辉 自制表格
		df0 = self.df[self.df.loc[:, 14].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 15].isin(self.num_list)]
		df0 = df0[df0.iloc[:, 16].isin(self.num_list)]
		# ---
		df0 = df0.loc[:, [1, 14, 15, 16, 17]]
		df0[17] = df0[17].fillna("-")
		df0.rename(columns={1: "供应商货号", 14: "数量", 15: "单价", 16: "金额", 17: "备注"}, inplace=True)
		df0 = self.groupbyagg(df0)
		msg = "test"
		return df0, msg
