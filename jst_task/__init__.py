from .database import JST_TASK
import datetime


kwargs={}

task = JST_TASK(**kwargs)

def default_task(mode="jst.orders.query", modified_time="", time_slot=""):
	config = {
		"jst.orders.query" : {"minutes":30},  # 订单列表
	}
	try:
		modified_time = datetime.datetime.strftime(modified_time, "%Y-%m-%d %H:%M:%S")
	except:
		modified_time = datetime.datetime.now()
	if not time_slot:
		time_slot = config["mode"]
	modified_time_begin = datetime.datetime.strftime(modified_time - datetime.timedelta(**time_slot), "%Y-%m-%d %H:%M:%S")
	modified_time_end = datetime.datetime.strftime(modified_time, "%Y-%m-%d %H:%M:%S")
	
	# main choose
	if mode=="shops.query":
		task.save_data()
		print(" - FINISHED!")
	elif mode=="sku.query":
		task.save_data()
		print(" - FINISHED!")
	elif mode=="inventory.query":
		task.save_data()
		print(" - FINISHED!")
	elif mode=="jst.orders.query":
		task.save_data(mode=mode, page_size=30, modified_begin=modified_time_begin, modified_end=modified_time_end)
		print(" - FINISHED!")
	else:
		print(" - DO NOTHING!")
