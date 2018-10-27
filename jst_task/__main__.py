import datetime

from jst_task.database import JST_TASK
from jst_task.view_task import VIEW_TASK
from jst_task.buffer import BUFFER_SQL

import configure
import pymysql

task = JST_TASK()


try:
    import sys
    argv = sys.argv[1]
    # argv = eval(argv)
except:
    argv = "jst.orders.query"



print(" -->:", argv)

def request_sql(mode='jst.orders.query', sql='xiaobaods_w'):
	conn = pymysql.connect(host=configure.echo(sql)["config"]["host"],
	                       user=configure.echo(sql)["config"]["user"],
	                       passwd=configure.echo(sql)["config"]["passwd"],
	                       db='baoersqlerp',
	                       port=configure.echo(sql)["config"]["port"],
	                       charset=configure.echo(sql)["config"]["charset"],
	                       )
	cur = conn.cursor()
	try:
		cur.execute("SELECT max(`modified`) FROM `{}`".format(mode))
		data = cur.fetchone()
	except Exception as e:
		print(e)
	finally:
		cur.close()
		conn.close()
	return data[0]

def create_timezone(begin, end, max_solt):
    timezone = [begin,]
    while end - begin > datetime.timedelta(max_solt):
        begin += datetime.timedelta(max_solt)
        timezone.append(begin)
    if begin != end:
        timezone.append(end)
    return timezone

def default_task(mode="jst.orders.query", modified_time=""):
	# 86400
	config = {
		"jst.orders.query" : 3,
		"shops.query": 3650, # 店铺查询
        "sku.query": 3, # 普通商品查询
        "inventory.query": 3,  # 实际库存查询
		"logistic.query": 3, # 发货信息查询
		"purchase.query": 3, # 采购单查询
		"purchasein.query": 3, # 采购进仓查询
		"jst.orders.out.query": 3, # 出库查询
		"purchaseout.query": 3, # 采购退货查询
		"jst.refund.query": 3,
	}
	try:
		modified_time = datetime.datetime.strftime(modified_time, "%Y-%m-%d %H:%M:%S")
	except:
		modified_time = datetime.datetime.now()
	# 判断超域
	time_zone = create_timezone(request_sql(mode), modified_time, config[mode])
	for i in range(len(time_zone) - 1 ):
		# 格式规整
		modified_time_begin = datetime.datetime.strftime(time_zone[i] , "%Y-%m-%d %H:%M:%S")
		modified_time_end = datetime.datetime.strftime(time_zone[i+1], "%Y-%m-%d %H:%M:%S")
		print("begin: {}".format(modified_time_begin))
		print("end: {}".format(modified_time_end))
		
		if mode in config:
			task.save_data(mode=mode, page_size=30, modified_begin=modified_time_begin, modified_end=modified_time_end)
			print(" - FINISHED!")
		else:
			print(" - DO NOTHING!")


# view3
if argv[0:4] == "view":
	if len(argv) == 4:
		date_length = 1
	else:
		date_length = int(argv[4:])
	view = VIEW_TASK(mode="daily_sales_result", date_length=date_length)
	view.run()
elif argv[0:5] == "store":
	if len(argv) == 5:
		date_length = 5
	else:
		date_length = int(argv[5:])
	view = VIEW_TASK(mode="daily_shop_sales", date_length=date_length)
	view.run()
elif argv[0:4] == "buff":
	buffer = BUFFER_SQL()
	buffer.run()
else:
	default_task(mode=argv)
