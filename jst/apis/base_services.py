# -*- coding: utf-8 -*-
from jst.util.rpc_client import RpcClient
from jst.apis.config import MODE

# 基础服务
# 默认载入时将对参数的运行结果传递给变量self.__client
# 类方法
# self.shops_query(nicks) 调用非奇门的方式，获取店铺信息
#   - nicks 店铺信息
# self.way_bill_get_new() 用奇门的方式获取订单信息
#   - params 参数集

class BaseService:

    __client = None

    def __init__(self, conf, msg):
        self.__client = RpcClient(conf)
        self.msg = msg

    def run(self, mode="shops.query", *args):
        if mode in MODE:
            if self.msg:
                print("arg: {}".format(args))
            mid_params = {}
            for i in MODE[mode]:
                if args[0].get(i, ""):
                    mid_params[i] = args[0][i]
            if mode == "shops.query":
                params = {"nicks": mid_params}
            else:
                params = mid_params
            return self.__client.call(mode, params, self.msg)
        else:
            return None

    # def shops_query(self, nicks=None, *args, **kwargs):   # 店铺查询
    #     return self.__client.call("shops.query", {"nicks": nicks})
    #
    # def logisticscompany_query(self, *args, **kwargs):   # 物流公司查询
    #
    #     return self.__client.call("logisticscompany.query", {})
    #
    # def jst_orders_query(self, params, *args, **kwargs):
    #
    #     return self.__client.call("jst.orders.query", params)

