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
		self.kwargs["mode"] = kwargs.get("mode", "daily_sales_result")
		if self.kwargs["mode"] == "daily_sales_result":
			self.kwargs["date_length"] = kwargs.get("date_length", 1)
		elif self.kwargs["mode"] == "daily_shop_sales":
			self.kwargs["date_length"] = kwargs.get("date_length", 3)
		self.kwargs["sql"] = kwargs.get("sql", "xiaobaods_w")
		self.kwargs["date"] = kwargs.get("date", datetime.datetime.strftime(datetime.datetime.now() -
		                                                datetime.timedelta(self.kwargs["date_length"]), "%Y-%m-%d"))
	
	def run(self):
		write_log = 1
		print("* SQL: {}; Date: {}; Length: {};".format(self.kwargs["sql"], self.kwargs["date"], self.kwargs["date_length"]))
		for date_length_run in range(self.kwargs["date_length"]+1):
			if self.kwargs["mode"] == "daily_sales_result":
				centence = self.return_sql_sentence(date_length=self.kwargs["date_length"]-date_length_run)
				log = self.save_to_sql(sql=self.kwargs["sql"], centence=centence)
				if write_log:
					self.save_to_sql(sql=self.kwargs["sql"], centence=self.return_sql_sentence(data=log, is_log=True),
									 db="baoersqlview", is_log=True)
			if self.kwargs["mode"] == "daily_shop_sales":
				centence = self.return_sql_sentence(date_length=self.kwargs["date_length"]-date_length_run)
				log = self.save_to_sql(sql=self.kwargs["sql"], centence=centence)
				if write_log:
					self.save_to_sql(sql=self.kwargs["sql"], centence=self.return_sql_sentence(data=log, is_log=True),
									 db="baoersqlview", is_log=True)
			write_log = 0
	
	def return_sql_sentence(self, data={}, date_length=1, is_log=False):
		'''
		生成对应的SQL语句
		'''
		if self.kwargs["mode"] == "daily_sales_result":
			if not is_log:
				sql_sentence = "REPLACE INTO baoersqlview.daily_sales_results SELECT T1.`shop_name` AS `shop`, DATE(T1.`order_date`) AS `date`,T1.`运营` AS `operator`,T1.`件数` AS `sale`,\
	T2.`人工单` AS `manual_sale`,T1.`销售额` AS `amount`,T2.`人工销售额` AS `manual_amount`, NOW() AS `refresh_time` FROM (SELECT O.shop_name,O.order_date,S.operator AS `运营`,COUNT( O.`o_id` ) AS `件数`,SUM( P.`amount`\
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
		if self.kwargs["mode"] == "daily_shop_sales":
			if not is_log:
				sql_sentence = "REPLACE INTO baoersqlview.daily_shop_sales SELECT `date`, `brand`, sum(`sale`) AS `sale`, NOW() AS `refresh_time` FROM baoersqlbs.bc_brand_granularity_sales WHERE " \
				               "date = '{0}' GROUP BY brand UNION ALL SELECT `date`, `brand`, sum(`sale`) AS `sale`, NOW() AS `refresh_time`" \
				               "FROM baoersqlbs.bc_owned_granularity_sales WHERE date = '{0}' GROUP BY brand ORDER BY `sale` DESC;".format(self.kwargs["date"])
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
