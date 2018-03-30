# -*- coding: utf-8 -*-
from  collections import OrderedDict

# 配置文件类
# 类参数：
# self.target_appkey ???
# self.__url_map = {
#           'jst': http://...
#           'qm': http://...
# }
# 类方法：
# self.get_request_url() 通过对self.sandbox的判断，调整默认url的状态

class Config:

    __url_map = OrderedDict({'jst':None,'qm':None})

    def __init__(self, sandbox, partner_id, partner_key, token, taobao_appkey, taobao_secret, target_appkey='23060081', *args, **kwargs):
        self.sandbox = sandbox
        self.partner_id = partner_id
        self.partner_key = partner_key
        self.token = token
        self.taobao_appkey = taobao_appkey
        self.taobao_secret = taobao_secret
        self.target_appkey = target_appkey
       
        
    def get_request_url(self):
        
        if self.sandbox:
            self.__url_map['jst'] = 'http://b.sursung.com/api/open/query.aspx'
            self.__url_map['qm'] = 'http://a1q40taq0j.api.taobao.com/router/qmtest'
            
        else:
            self.__url_map['jst'] = 'http://open.erp321.com/api/open/query.aspx'
            self.__url_map['qm'] = 'http://a1q40taq0j.api.taobao.com/router/qm'
            
        return self.__url_map
            
    
    