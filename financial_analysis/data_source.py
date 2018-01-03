#!usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import requests
import configure

class caibaoshuo():
    '''
    数据来源：caibaoshuo.cn API
    '''

    def __init__(self, api_name="caibaoshuo"):
        '''
        在 caibaoshuo.cn 稳定情况下，不需要传递任何参数
        '''
        self._api_token = configure.echo(api_name)["config"]["api"]

    def request(self, sheets: str="mj", index_key: str="000001"):
        '''
        Parameter:
        - sheets(str):
            - cp: company_information 公司信息
            - mj: financial_analysis_table 财务分析表
            - bs: balance_sheets 资产负债表
            - pl: income_statements 利润表
            - cf: cash_flow_statements 现金流量表
        - index_key(str):
            - 000000: 全部公司信息
            - 000001: 例：中国平安
        '''
        part = {"c": "companies","cp": "companies", "company_information": "companies",
                "f": "mjanalyses", "mj": "mjanalyses", "financial_analysis_table": "mjanalyses",
                "b": "bssheets", "bs": "bssheets", "balance_sheets": "bssheets",
                "i": "plsheets", "pl": "plsheets", "income_statements": "plsheets",
                "c": "cfsheets", "cf": "cfsheets", "cash_flow_statements": "cfsheets"
               }
        if sheets not in part:
            sheets = "mj"
            index_key="000001"
        if part[sheets] == "companies" and index_key == "000000":
            url = "http://caibaoshuo.com/api/v1/companies?auth_token=" +\
            self._api_token
        else:
            url = "http://caibaoshuo.com/api/v1/" + part[sheets] + "/" +\
            index_key + "?auth_token=" + self._api_token
        # requests
        response = requests.get(url)
        return eval(response.text.replace("null", "np.nan"))
