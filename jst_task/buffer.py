# -*- coding: utf-8 -*-
#!/usr/bin/python

import pymysql
import configure
import datetime
from jst_task.config import BUFFER_SQL_LIST, BUFFER_CHINESE_VARIABLE

__author__ = 'envisocy'
__date__ = '2018/7/30 13:53'

class BUFFER_SQL():
	def __init__(self):
		pass
	
	
	def run(self, sql="xiaobaods_w", db="baoersqlbs"):
		print("*** Buffer Run ***")
		for table in BUFFER_SQL_LIST:
			if table in BUFFER_CHINESE_VARIABLE:
				variable = "日期"
			else:
				variable = "date"
			print("*** Table:", table, " ***")
			# 查询日期
			centence = "SELECT min(`" + variable + "`) FROM " + table + ";"
			date_min = self.request_to_sql(sql, centence, db)[0][0]
			date_tag = datetime.datetime.now().date() - datetime.timedelta(90)
			date_hold = datetime.datetime.now().date() - datetime.timedelta(104)
			date_range_delete = self.date_range(date_min, date_hold)
			date_range_hold = self.date_range(date_hold, date_tag)
			error_message = self.transfer(date_range_delete, sql, db, table, True, variable)
			error_message += self.transfer(date_range_hold, sql, db, table, False, variable)
			# 写入日志
			if error_message:
				result = error_message
			else:
				result = "OK!"
			if not date_range_delete:
				date_range_delete = ["2000-01-01"]
			if not date_range_hold:
				date_range_hold = ["2000-01-01"]
			log = {
				"datetime": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
				"table": table,
				"date_range_delete_begin": min(date_range_delete),
				"date_range_delete_end": max(date_range_delete),
				"date_range_hold_begin": min(date_range_hold),
				"date_range_hold_end": max(date_range_hold),
				"result": result,
			}
			centence = self.create_log_centence(log)
			self.request_to_sql(sql, centence, db)
			
	def transfer(self, date_list, sql, db, table, delete=False, variable="date"):
		error_message = ""
		for date in date_list:
			# 查询原始条目数
			centence = "SELECT COUNT(*) FROM " + table + " WHERE `" + variable + "`='" + date + "';"
			raw_count = self.request_to_sql(sql, centence, db)[0][0]
			# 插入条目
			centence = "REPLACE INTO " + table + "_OLD SELECT * FROM " + table + " WHERE `" + variable + "`='" + date + "';"
			self.request_to_sql(sql, centence, db)
			# 查询OLD表条目
			centence = "SELECT COUNT(*) FROM " + table + "_OLD WHERE `" + variable + "`='" + date + "';"
			old_count = self.request_to_sql(sql, centence, db)[0][0]
			# 判断是否完成
			if raw_count==old_count:
				if delete==True:
					centence = "DELETE FROM " + table + " WHERE `" + variable + "`='" + date + "';"
					self.request_to_sql(sql, centence, db)
					# centence = "optimize table " + table + ";"
					# self.request_to_sql(sql, centence, db)
			else:
				error_message += "- {}: {}/{} Error write;".format(date, old_count, raw_count)
		# 重新整理表单数据缓存 !!! 需要锁表
		centence = "optimize table " + table + ";"
		self.request_to_sql(sql, centence, db)
		return error_message
		
	
	def date_range(self, begin, end):
		date_list = []
		if end > begin:
			begin = datetime.datetime.strftime(begin, "%Y-%m-%d")
			end = datetime.datetime.strftime(end, "%Y-%m-%d")
			while begin != end:
				date_list.append(begin)
				begin = datetime.datetime.strftime(
					datetime.datetime.strptime(begin, "%Y-%m-%d") + datetime.timedelta(1), "%Y-%m-%d")
		return date_list
		
	def request_to_sql(self, sql, centence, db="baoersqlerp"):
		data = None
		conn = pymysql.connect(host=configure.echo(sql)["config"]["host"],
		                       user=configure.echo(sql)["config"]["user"],
		                       passwd=configure.echo(sql)["config"]["passwd"],
		                       db=db,
		                       port=configure.echo(sql)["config"]["port"],
		                       charset=configure.echo(sql)["config"]["charset"],
		                       )
		cur = conn.cursor()
		try:
			cur.execute(centence)
			conn.commit()
			data = cur.fetchall()
		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()
		return data
		
	def create_log_centence(self, log):
		return "INSERT INTO `{}` {} VALUES{} ;".format("transfer_task_log"
					, str([i for i in log.keys()]).replace("[","(").replace("]",")").replace("'","`"),
	str([str(i).replace("'","").replace('"','') for i in log.values()]).replace("[","(").replace("]",")").replace('"',"'"))
	
