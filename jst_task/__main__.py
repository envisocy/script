import datetime

from jst_task.database import JST_TASK


task = JST_TASK()

try:
    import sys
    argv = sys.argv[1]
    # argv = eval(argv)
except:
    argv = "jst.orders.query"

print(" -->:", argv)

def default_task(mode="jst.orders.query", modified_time="", time_slot=""):
	config = {
		"jst.orders.query" : {"hours": 1},
		"shops.query": {"days": 1}, # 店铺查询
        "sku.query": {"hours": 1}, # 普通商品查询
        "inventory.query": {"hours": 1},  # 实际库存查询
		"logistic.query": {"hours": 1}, # 发货信息查询
		"purchase.query": {"hours": 1}, # 采购单查询
		"purchasein.query": {"hours": 1}, # 采购进仓查询
		"jst.orders.out.query": {"hours": 1}, # 出库查询
		"purchaseout.query": {"hours": 1}, # 采购退货查询
		"jst.refund.query": {"hours": 1}
	}
	try:
		modified_time = datetime.datetime.strftime(modified_time, "%Y-%m-%d %H:%M:%S")
	except:
		modified_time = datetime.datetime.now()
	if not time_slot:
		time_slot = config[mode]
	modified_time_begin = datetime.datetime.strftime(modified_time - datetime.timedelta(**time_slot), "%Y-%m-%d %H:00:00")
	modified_time_end = datetime.datetime.strftime(modified_time, "%Y-%m-%d %H:00:00")
	
	if mode in config:
		task.save_data(mode=mode, page_size=30, modified_begin=modified_time_begin, modified_end=modified_time_end)
		print(" - FINISHED!")
	else:
		print(" - DO NOTHING!")


default_task(mode=argv)