# -*- coding: utf-8 -*-

import hashlib
import json
import time
from collections import OrderedDict
from wheel.signatures import sign


try:
    from urllib2 import urlopen, Request
    from urlparse import urlparse
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.parse import urlparse, urlencode

# 调用服务端进行处理
# 默认载入时必须传入cfg配置：cfg为Config类
# self.get_request_url(params) 根据params["method"]，返回具体的url
# self.get_system_params(action, params=None) 根据参数更新system_params中的sign和jstsign
#   # 默认载入系统参数，其中method为传入的action
#   # 如果jst在method中，将系统变量更新（添加淘宝app_key）
#   # 将新的系统变量system_params返回给generate_signature()
# self.generate_signature(system_params, params=None)
#   # 对系统变量system_params进行排序(order)
#   # 如果jst在system_params['method']内
#   #   # method为调换掉system_params['method']中jst.
#   #   # 计算jstsign
#   #   # 将计算的MD5加密后的jstsign加入system_params
#   #   # 合并params和system_params字典并排序
#   #   # 切分并遍历字符串，MD5加密后，得到sign，加入system_params
#   # 返回system_params
#   # 否则的话，常规的非奇门访问方式
# self.post(url, data, url_params, action) 访问
#   # url URL地址
#   # data 非jst.状态下的POST(对应非jst.状态下的查询参数)
#   # url_params jst.状态下的GET包装
#   # action 类似method?

class RpcClient:
    
    def __init__(self, cfg):
        self.config = cfg        

    def call(self, action, parameters, msg=False):

        if msg:
            print("action: {}\nparameters: {}\n".format(action, parameters))
        
        system_params = self.get_system_params(action, params= parameters)
        
        request_url = self.get_request_url(system_params)

        if msg:
            print("Request Params: \nrequest_url: {}\nparameters: {}\nsystem_params: {}\naction: {}\n".format(
				request_url, parameters, system_params, action
			))
        
        result = self.post(request_url, parameters, system_params, action)

        return result
    
    
    def get_request_url(self, params):
        
        url_map = self.config.get_request_url()
        
        return url_map['qm'] if 'jst' in params['method'] else url_map['jst']
        
#  
    def generate_signature(self, system_params, params = None):
        sign_str = ''
        system_params = OrderedDict(sorted(system_params.items(), key = lambda e:e[0],reverse=False))
        
        if 'jst' in system_params['method']:
            method = system_params['method'].replace('jst.', '')
            #计算jstsign
            jstsign = method+self.config.partner_id+"token"+self.config.token+"ts"+str(system_params['ts'])+self.config.partner_key
            hl = hashlib.md5(jstsign.encode('utf-8'))
            system_params['jstsign'] = hl.hexdigest()
            
            #合并字典
            if params:
                system_params = dict(params, **system_params)
            
            system_params = OrderedDict(sorted(system_params.items(), key = lambda e:e[0],reverse=False)) 
            for k,v in system_params.items():
                #如果是list则切分
                if isinstance(v, list):
                    sign_str += "%s%s"%(k,','.join(v))
                    continue
                    
                sign_str += "%s%s"%(k,str(v))
            
            hll = hashlib.md5((self.config.taobao_secret+sign_str+self.config.taobao_secret).encode("utf-8"))
            
            system_params['sign'] = hll.hexdigest().upper()
        else:
            sign_str = system_params['method']+system_params['partnerid']
            for k,v in system_params.items():
                if k in ['method','sign','partnerid','partnerkey'] : continue
                sign_str += "%s%s"%(k,str(v))
            
            sign_str +=self.config.partner_key
            
            hl = hashlib.md5((sign_str).encode("utf-8"))
            system_params['sign'] = hl.hexdigest()
    
        return system_params

    """
            获取系统参数
    """
    def get_system_params(self, action, params = None):
        #默认系统参数
        system_params = {
            'partnerid':self.config.partner_id,
            'token': self.config.token,
            'method': action,
            'ts': int(time.time())
        }
        
        if 'jst' in action:
            
            system_params['sign_method'] = 'md5'
            system_params['format'] = 'json'
            system_params['app_key'] = self.config.taobao_appkey
            system_params['timestamp'] = time.strftime("%Y-%m-%d %X", time.localtime())
            system_params['target_app_key'] = self.config.target_appkey
        
        return self.generate_signature(system_params, params= params)
    
        
    def post(self, url, data, url_params, action):
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            post_data = None
            
            #发送前的处理
            if 'jst.' not in action:
                post_data = json.dumps(data).encode('utf-8')
            else:
                for k,v in url_params.items():
                    if isinstance(v, list):
                        url_params[k] = ','.join(v)
                    
            url+= '?'+urlencode(url_params)
            request = Request(url, post_data, headers)
            response = urlopen(request)
            result = response.read()
            return json.loads(result.decode('utf-8'))
        except Exception as e:
            print(e.message)
