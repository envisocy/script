import requests
import hashlib
import time
import json


class jushuitan(object):
    def __init__(self):
        self.__parameter = {
                "PartnerId": "ywv5jGT8ge6Pvlq3FZSPol345asd",# 合作方编号
                "PartnerKey": "ywv5jGT8ge6Pvlq3FZSPol2323",# 接入秘钥
                "TOKEN": "181ee8952a88f5a57db52587472c3798",# 授权码
                "method": "shops.query", # 接口名称
                "ts": str(int(time.time())), # 请求时间
            }
        self.__parameter["sign"] = self.create_sign(method=self.__parameter["method"])

    def create_sign(self, method):
        if method:
            sign_method = method
        else:
            sign_method = self.__parameter["method"]
        sign_content = sign_method + self.__parameter["PartnerId"] + "ts" + self.__parameter["ts"] + \
            "token" + self.__parameter["TOKEN"] + self.__parameter["PartnerKey"]
        return hashlib.md5(sign_content.encode("utf-8")).hexdigest()

    def get_data(self, method="", content=""):
        params = {
            "ts": self.__parameter["ts"],
            "partnerid": self.__parameter["PartnerId"],
            "method": self.__parameter["method"],
            "token": self.__parameter["TOKEN"],
            "sign": self.__parameter["sign"],
        }
        if method:
            params["method"] = method
            params["sign"] = self.create_sign(method)
        if content:
            r = requests.post("http://b.sursung.com/api/open/query.aspx", params=params, data=content).text
        else:
            r = requests.get("http://b.sursung.com/api/open/query.aspx", params=params).text
        return json.loads(r)

    def get_table(self, method="", content=""):
        import pandas as pd
        dic = self.get_data(method, content)
        return pd.DataFrame(dic["datas"])

    def _pr(self): # test
        print(self.__parameter)
