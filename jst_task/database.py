import jst
import pymysql
import configure
from datetime import datetime
from copy import deepcopy
import time

from jst_task.config import *

config = {
    "shops.query": {"income": "common", "data": "shops" ,"has_next": False, "sleep": 0.1}, # 店铺查询
    "sku.query": {"income": "common", "data": "datas" ,"has_next": True, "sleep": 0.1}, # 普通商品查询
    "inventory.query": {"income": "common", "data": "inventorys" ,"has_next": True, "sleep": 0.2},  # 实际库存查询
	"jst.orders.query": {"income": "magic", "data": "orders", "has_next": True, "sleep": 0.2, "sublist": ["items", "pays"]}, # 订单查询
	"logistic.query": {"income": "common", "data": "orders", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 发货信息查询
	"purchase.query": {"income": "common", "data": "datas", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 采购单查询
	#"supplier.query": {"income": "common", "data": "datas" ,"has_next": False, "sleep": 0.1}, # 供应商查询 验证失败
	"purchasein.query": {"income": "common", "data": "datas", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 采购进仓查询
	"jst.orders.out.query": {"income": "magic", "data": "datas", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 出库查询
	"purchaseout.query": {"income": "common", "data": "datas", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 采购退货查询
	"jst.refund.query": {"income": "magic", "data": "datas", "has_next": True, "sleep": 0.2, "sublist": ["items"]}, # 退货退款查询
}

class JST_TASK():
	'''
	get_data 仅查询对应的数据
	save_data 查询并存入数据库
	'''
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.kwargs["msg"] = self.kwargs.get("msg", False)
		self.kwargs["page"] = self.kwargs.get("page", 10)
		self.kwargs["mode"] = self.kwargs.get("mode", "sku.query")
	
	def save_data(self, sql="xiaobaods_w", db="baoersqlerp", **kwargs):
		'''
		数值部分
		'''
		data = self.get_data(**kwargs)  # 获取data
		# 核心部分
		if data:
			data0 = deepcopy(data)
			for item in data0:
				# 刷单判断
				if self.kwargs["mode"]=="jst.orders.query" and item.get("question_type", "")=="特殊单":
					ss_data = [{"o_id": item["o_id"], "create_date": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
					            "pay_amount": item["pay_amount"], "order_date": item["order_date"],
					            "pay_date": item["pay_date"], "remark": item.get("remark"),
					            "shop_name": item["shop_name"],
					            "question_desc": item.get("question_desc"), "question_type": item.get("question_type"),}]
					ss_sentence = self.return_sql_sentence(data=ss_data, table="jst.orders.query.special_single")
					self.save_to_sql(sql, ss_sentence, db=db, length=0)
				# 排除特殊订单
				for key in config[self.kwargs["mode"]].get("sublist", []):
					del item[key]
			data0_sql = self.return_sql_sentence(data=data0, table=self.kwargs["mode"])
			log = self.save_to_sql(sql, data0_sql, db=db, length=len(data0))
			# 核心部分储存日志
			self.save_to_sql(sql, self.return_sql_sentence(data=log, table="ERP_task_log", is_log=True), db=db, is_log=True)
			# 支表部分
			for sublist in config[self.kwargs["mode"]].get("sublist", []):
				data1 = []
				for item in data:
					for i in range(len(item.get(sublist, []))):
						if item.get(sublist):   # 排除可能为None的情况
							if item.get("o_id"):
								data1_o_id = {"o_id": str(item.get("o_id"))}
								item.get(sublist, [])[i].update(data1_o_id)
						data1.extend(item.get(sublist, []))
				data1_sql = self.return_sql_sentence(data1, table=self.kwargs["mode"] + "." + sublist)
				log = self.save_to_sql(sql, data1_sql, len(data1), db=db, add_mode="." + sublist)
				self.save_to_sql(sql, self.return_sql_sentence(data=log, table="ERP_task_log", is_log=True), db=db, is_log=True)
		else:
			log = self.create_log(sql, "baoersqlerp")
			log["result"] = "None"
			self.save_to_sql(sql, self.return_sql_sentence(data=log, table="ERP_task_log", is_log=True), db=db, is_log=True)
	
	
	def return_sql_sentence(self, data, table, is_log=False):
		'''
		生成对应的SQL语句
		'''
		if not is_log:
			sql_sentence = ""
			for item in data:
				for rule in FIELD_RULE:     # 增加长度判定
					if item.get(rule):
						if len(str(item.get(rule))) > FIELD_RULE[rule]:
							item[rule] = str(item[rule])[:FIELD_RULE[rule]]
				keys_sentence = str([i for i in item.keys()])[1:-1].replace("'","`")
				values_sentence = "({}),".format(str([str(i).replace("'","").replace('"','') for i in
													  item.values()])[1:-1].replace("'",'"'))
				values_sentence = values_sentence[:-1]  # 取出末尾的,
				sql_sentence += "REPLACE INTO `{}` ({}) VALUES{} ;".format(table, keys_sentence, values_sentence)
			return sql_sentence
		else:   # log
			sql_sentence = "INSERT INTO `{}` ({}) VALUES({}) ;".format(
				table, str([i for i in data.keys()])[1:-1].replace("'","`"),
				str([str(i).replace("'","").replace('"','') for i in data.values()])[1:-1].replace('"',"'")
			)
			return sql_sentence
			
	
	def save_to_sql(self, sql, sentence, length=-1, add_mode="", db="baoersqlerp", is_log=False):
		'''
		length 专为日志文件写入文件长度
		'''
		conn = pymysql.connect(host=configure.echo(sql)["config"]["host"],
		                       user=configure.echo(sql)["config"]["user"],
		                       passwd=configure.echo(sql)["config"]["passwd"],
		                       db=db,
		                       port=configure.echo(sql)["config"]["port"],
		                       charset=configure.echo(sql)["config"]["charset"],
		                       )
		cur = conn.cursor()
		if not is_log:
			log = self.create_log(sql=sql, db=db, add_mode=add_mode)
			log["length"] = length
		try:
			cur.execute(sentence)
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
		
	def get_data(self, **kwargs):
		'''
		通过调用外部jst包
		支持所有本页config项目
		输出完整的api返回数据的数值部分
		'''
		self.kwargs.update(kwargs)
		# Initialization Parameters
		has_next = True
		code = 1
		data = []
		times = 0 # 过热保护
		error = 0
		self.kwargs["page_index"] = 1   # 重置翻页系数为1
		while has_next:
			# Read Cycle
			while code:
				if times > 5:
					break
					error = 1
				times += 1
				message = jst.run(**self.kwargs)
				code = message.get("code", 0)
				time.sleep(config[self.kwargs["mode"]]["sleep"])
			code = 1 # Initialization the Read Cycle
			times = 0 # 重置过热保护
			if error:
				return "Error!"
			if config[self.kwargs["mode"]]["income"] == "magic":
				if config[self.kwargs["mode"]]["has_next"]==True:
					has_next = message["response"].get("has_next")
				else:
					has_next = False
				if message["response"].get(config[self.kwargs["mode"]]["data"]):
					data.extend(message["response"][config[self.kwargs["mode"]]["data"]])
			elif config[self.kwargs["mode"]]["income"] == "common" and message.get(config[self.kwargs["mode"]]["data"]) != None:
				if config[self.kwargs["mode"]]["has_next"]==True:
					has_next = message.get("has_next")
				else:
					has_next = False
				if message.get(config[self.kwargs["mode"]]["data"]):
					data.extend(message[config[self.kwargs["mode"]]["data"]])
			else:
				break
			self.kwargs["page_index"] = self.kwargs.get("page_index", 1) + 1
		# 初始化
		self.kwargs["page_index"] -= 1  # 为了正确显示log具体的页数
		return data

	def create_log(self, sql, db, add_mode=""):
		return {
			"datetime": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
			"mode": self.kwargs["mode"] + add_mode,
			"parameter": str(self.kwargs),
			"sql": sql,
			"db": db,
			"length": -1,
			"result": ""
		}

