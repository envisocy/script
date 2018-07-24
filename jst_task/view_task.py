# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'envisocy'
__date__ = '2018/7/24 16:29'

import pymysql
import datetime
import configure

class VIEW_TASK():
	def __init__(self, **kwargs):
		self.kwargs = {}
		self.kwargs["date_length"] = kwargs.get("date_length", 1)
		self.kwargs["mode"] = kwargs.get("mode", "daily_sales_result")
		self.kwargs["sql"] = kwargs.get("sql", "xiaobaods_w")
	
	def run(self):
		if self.kwargs["mode"] == "daily_sales_result":
			centence = self.return_sql_sentence(date_length=self.kwargs["date_length"])
			print(self.kwargs["sql"])
			log = self.save_to_sql(sql=self.kwargs["sql"], centence=centence)
			self.save_to_sql(sql=self.kwargs["sql"], centence=self.return_sql_sentence(data=log, is_log=True),
			                 db="baoersqlview", is_log=True)
	
	def return_sql_sentence(self, data={}, date_length=1, is_log=False):
		'''
		生成对应的SQL语句
		'''
		if not is_log:
			sql_sentence = "INSERT INTO baoersqlview.daily_sales_results SELECT T1.`shop_name` AS `店铺`,DATE(T1.`order_date`) AS `日期`,T1.`运营`,T1.`件数`,\
T2.`人工单`,T1.`销售额`,T2.`人工销售额` FROM (SELECT O.shop_name,O.order_date,S.operator AS `运营`,COUNT( O.`o_id` ) AS `件数`,SUM( P.`amount`\
) AS `销售额` FROM `jst.orders.query` AS O INNER JOIN `jst.orders.query.items` AS I ON O.o_id = I.o_id INNER JOIN `jst.orders.query.pays` AS P \
ON O.o_id = P.o_id INNER JOIN `shops.query` AS S ON O.shop_name = S.shop_name WHERE O.`order_date` >= DATE_SUB( CURDATE( ), INTERVAL {0} DAY ) \
AND O.`order_date` < DATE_SUB( CURDATE( ), INTERVAL {1} DAY ) GROUP BY O.shop_name ) AS T1 LEFT JOIN ( SELECT N.shop_name, COUNT( N.`o_id` ) AS \
`人工单`,SUM( N.`pay_amount` ) AS `人工销售额` FROM `jst.orders.query.special_single` AS N WHERE N.`order_date` >= DATE_SUB( CURDATE( ), \
INTERVAL {0} DAY ) AND N.`order_date` < DATE_SUB( CURDATE( ), INTERVAL {1} DAY ) GROUP BY N.shop_name ) AS T2 ON T1.shop_name = T2.shop_name \
GROUP BY T1.shop_name ORDER BY `件数` DESC;".format(date_length, date_length - 1)
			return sql_sentence
		else:   # log
			sql_sentence = "INSERT INTO `{}` ({}) VALUES({}) ;".format("view_task_log"
				, str([i for i in data.keys()])[1:-1].replace("'","`"),
				str([str(i).replace("'","").replace('"','') for i in data.values()])[1:-1].replace('"',"'")
			)
			return sql_sentence
	
	def save_to_sql(self, sql, centence, db="baoersqlerp", is_log=False):
		conn = pymysql.connect(host=configure.echo(sql)["config"]["host"],
		                       user=configure.echo(sql)["config"]["user"],
		                       passwd=configure.echo(sql)["config"]["passwd"],
		                       db=db,
		                       port=configure.echo(sql)["config"]["port"],
		                       charset=configure.echo(sql)["config"]["charset"],
		                       )
		cur = conn.cursor()
		if not is_log:
			log = self.create_log(sql=sql, db=db)
		try:
			cur.execute(centence)
			conn.commit()
			if not is_log:
				log["result"] = "OK!"
		except Exception as e:
			print(e)
			if not is_log:
				log["result"] = str(e)[:254]
		finally:
			cur.close()
			conn.close()
		if not is_log:
			return log
		
	def create_log(self, sql, db):
		return {
			"datetime": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
			"date": datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(self.kwargs["date_length"]), "%Y-%m-%d"),
			"mode": self.kwargs["mode"],
			"parameter": str(self.kwargs),
			"sql": sql,
			"db": db,
			"length": -1,
			"result": ""
		}
