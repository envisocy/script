# -*- coding: utf-8 -*-

from jst.apis.base_services import BaseService
from jst.config import Config

import configure


file_name = "jst_private"

env = {
    'sandbox': False, # 是否为沙盒环境
    'partner_id': configure.echo(file_name)["config"]["partner_id"],
    'partner_key': configure.echo(file_name)["config"]["partner_key"],
    'token': configure.echo(file_name)["config"]["token"],
    'taobao_appkey': configure.echo(file_name)["config"]["taobao_appkey"],
    'taobao_secret': configure.echo(file_name)["config"]["taobao_secret"],
}

if __name__ == '__main__':
    
    cfg = Config(**env)     # 配置参数
    service = BaseService(cfg, msg=True)      # 运行服务

    params = {
        'shop_id': '10127848',
        'modified_begin': '2018-04-18 00:00:00',
        'modified_end': '2018-04-18 12:00:00',
        'page_size': 10,
        'page_index': 1,
        # 'so_ids': ['111902591572215654']
    }


    # print(service.jst_orders_query(params))
    # print(service.shops_query(params))
    # print(service.logisticscompany_query())
    print(service.run('jst.orders.query', params))