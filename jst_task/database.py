import jst

config = {
    "shops.query": {"income": "common", "data": "shops" ,"has_next": False, "sleep": 0.1},
    "sku.query": {"income": "common", "data": "datas" ,"has_next": True, "sleep": 0.1},
    "inventory.query": {"income": "common", "data": "inventorys" ,"has_next": True, "sleep":0.2},
    
}

class JST_TASK():
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.kwargs["msg"] = self.kwargs.get("msg", False)
		self.kwargs["page"] = self.kwargs.get("page", 10)
		self.kwargs["mode"] = self.kwargs.get("mode", "sku.query")

	def add(self):
		pass

	def save(self):
		pass

	def get_data(self, **kwargs):
		self.kwargs.update(kwargs)
		import time
		# Initialization Parameters
		has_next = True
		code = 1
		data = []
		times = 0 # 过热保护
		error = 0
		while has_next:
			# Read Cycle
			while code:
				print("->code cycle:", code, times)
				if times > 5:
					break
					error = 1
				times += 1
				message = jst.run(**self.kwargs)
				code = message.get("code", 0)
				time.sleep(0.1)
			print("->before:", code, times)
			code = 1 # Initialization the Read Cycle
			times = 0 # 重置过热保护
			print("->past:", code, times)
			if error:
				return "Error!"
			if config[self.kwargs["mode"]]["income"] == "magic":
				if config[self.kwargs["mode"]]["has_next"]==True:
					has_next = message["response"]["has_next"]
				else:
					has_next = False
				data.extend(message["response"][config[self.kwargs["mode"]]["data"]])
			elif config[self.kwargs["mode"]]["income"] == "common":
				if config[self.kwargs["mode"]]["has_next"]==True:
					has_next = message["has_next"]
				else:
					has_next = False
				data.extend(message[config[self.kwargs["mode"]]["data"]])
			self.kwargs["page_index"] = self.kwargs.get("page_index", 1) + 1
		return data
