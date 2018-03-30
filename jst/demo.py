# -*- coding: utf-8 -*-

from jst.apis.base_services import BaseService
from jst.config import Config


env = {
        'sandbox':True, # 是否沙盒环境
        'partner_id':'ywv5jGT8ge6Pvlq3FZSPol345asd',    # partner_id
        'partner_key':'ywv5jGT8ge6Pvlq3FZSPol2323',     # partner_key
        'token': '181ee8952a88f5a57db52587472c3798',    # token
        'taobao_appkey': '24796332',                    # qm: taobao_appkey
        'taobao_secret': '667ecbdec1355f5bdd92b3ac2c710187'     # secret: taobao_secret
        
}



if __name__ == '__main__':
    
    cfg = Config(**env)     # 配置参数
    service = BaseService(cfg)      # 运行服务

    params = {
        'page_size':10,
        'page_index':1,
        'so_ids':['111902591572215654']
    }
    
    print(service.way_bill_get_new(params))