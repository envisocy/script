# -*- coding: utf-8 -*-
from jst.util.rpc_client import RpcClient

# 基础服务
# 默认载入时将对参数的运行结果传递给变量self.__client
# 类方法
# self.shops_query(nicks) 调用非奇门的方式，获取店铺信息
#   - nicks 店铺信息
# self.way_bill_get_new() 用奇门的方式获取订单信息
#   - params 参数集

class BaseService:

    __client = None

    def __init__(self, conf):
        self.__client = RpcClient(conf)

    def shops_query(self, nicks = None, *args, **kwargs):
       
        return self.__client.call("shops.query", {"nicks": nicks})

    def way_bill_get_new(self, params, *args, **kwargs):
       
        return self.__client.call("jst.orders.query", params) 

