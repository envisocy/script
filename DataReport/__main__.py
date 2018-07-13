# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018-06-10 10:34'

import sys


from DataReport.tidying import FILE_TIDYING
from DataReport.format import FORMATTED_DATA
from DataReport.report import REPORT_GENERATION
from DataReport.analysis import DATA_ANALYSIS

explan ='''
	Terminal中，第一个参数是mode, 第二个参数是date, 第三个参数是path, 第四个是detail
'''
mode_range = [
	"vendor_bill", "financial_store",
]

parameter = {}

### 运行传入参数：
parameter = {
	"date": "2018-07-11",
}


def run(**kwargs):
	mode = kwargs.get("mode", "vendor_bill")
	print(" * mode = ", mode)
	print(" * --- step0: Finished! ---")
	# step1: tidying：
	tidying = FILE_TIDYING(**kwargs)
	check_dict = tidying.run()
	if check_dict == None:
		return None
	kwargs.update(check_dict)
	print(" * >>> Step1: 文件整理结束！")
	for key,value in check_dict.items():
		if key != "文件列表：":
			print(" * {} {}".format(key,value))
	print(" * --- step1: Finished! ---")
	formatted = FORMATTED_DATA(**kwargs)
	df = formatted.run()
	print(" * >>> Step2: 文件归纳结束！")
	report = REPORT_GENERATION(df, **kwargs)
	report_paper, df = report.run()
	print(" * 核对结果：")
	print(report_paper)
	df.to_csv(r"C:\Users\Administrator\Desktop\result.csv")
	return df

if __name__ == '__main__':
	if not parameter:
		parameter_values = sys.argv[1:]
		parameter_keys = ["mode", "date", "path", "detail"][:len(sys.argv[1:])]
		parameter = dict(zip(parameter_keys, parameter_values))
	if parameter.get("mode", "") not in mode_range:
		parameter["mode"] = "vendor_bill"
	print(" * >>> Step0: 参数传入：", parameter)
	
	run(**parameter)
