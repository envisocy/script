import pandas as pd
import pymysql
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from financial_analysis.config import *

class caibaoshuo():
    '''
    caibaoshuo.cn API 2018
    '''

    def __init__(self, data_sources="caibaoshuo"):
        import configure
        if data_sources=="caibaoshuo":
            self._api_token = configure.echo(data_sources)["config"]["api"]
        else:
            self.sql = configure.echo(data_sources)["config"]

    def get_data(self, sheets="mj", code="000001"):
        '''
        Parameter:
        - sheets(str):
            - cp: company_information 公司信息
            - mj: financial_analysis_table 财务分析表
            - bs: balance_sheets 资产负债表
            - pl: income_statements 利润表
            - cf: cash_flow_statements 现金流量表
        - code(str):
            - 000000: 全部公司信息
            - 000001: 例：中国平安
        '''
        # "cp" 为1.0版本的接口，1.1版本沿用
        # "oj" 为1.0版本的接口
        # "mj" 为1.1版本的接口，添加了两个变量，但未测试通过
        # "bl","ic","cf" 为1.0版本接口，不知道会不会弃用
        part = {"cp": "companies", "company_information": "companies",
                "oj": "mjanalyses",
                "mj": "genealsheets", "financial_analysis_table": "genealsheets",
                "bl": "bssheets", "balance_sheets": "bssheets",
                "ic": "plsheets", "income_statements": "plsheets",
                "cf": "cfsheets", "cash_flow_statements": "cfsheets"
               }
        if sheets not in part:
            sheets = "mj"
            code="000001"
        if part[sheets] == "companies" and code == "000000":
            url = "http://caibaoshuo.com/api/v1/companies?auth_token=" + self._api_token
        else:
            url = "http://caibaoshuo.com/api/v1/" + part[sheets] + "/" + code + "?auth_token=" + self._api_token
        # requests
        response = requests.get(url)
        if response.status_code == 200:
            return eval(response.text.replace("null", "0"))['data']
        else:
            print(response.status_code)
            return None

    def industry_list(self, industry="互联网", companies=""):
        '''
        通过行业返回列表
        '''
        if not companies:
            companies = self.get_data("cp", "000000")
        df = pd.DataFrame(companies)
        if industry:
            return df.loc[df["industry"] == industry, "code"].tolist()
        else:
            return df.loc[:, "code"].tolist()

    def request_list(self, code="000002"):
        '''
        通过code返回列表
        '''
        companies = self.get_data(sheets="cp", code="000000")
        if code=="000000" or code=="":
            return self.industry_list(industry="", companies=companies)
        else:
            df = pd.DataFrame(companies)
            industry = df.loc[df["code"] == code,"industry"].iloc[0]
            return self.industry_list(industry=industry, companies=companies)

    def list_to_df(self, code_list, sheets="mj", variable="grossMargin_ratio"):
        import time
        df = pd.DataFrame()
        for code in code_list:
            print(" * 请求:" + code + "中...(共" + str(code_list.index(code) + 1) + "/" + str(len(code_list)) +"项)")
            df_code = pd.DataFrame(self.get_data(sheets=sheets, code=code))
            if not len(df_code):
                continue
            df_code = df_code.loc[:,["end_year", variable]]
            df_code["code"] = code
            df = pd.concat([df,df_code],axis=0)
            time.sleep(5)
        return df

    def swarmplot(self, code="000002", sheets="mj", variable="grossMargin_ratio"):
        variable_name = caibaoshuo_geneal_sheets_columns.get(variable, variable)
        print(" * 请求行业数据 ...")
        industry_list = self.request_list(code=code)
        print(" * 得到行业列表 ...")
        df = self.list_to_df(code_list=industry_list, sheets=sheets, variable=variable)
        print("绘图中")
        df.rename(columns={"end_year":"年报年份", variable:variable_name}, inplace=True)
        df[variable_name + "分布"] = "行业状况"
        df.loc[df["code"]==code,variable_name+"分布"]=code
        sns.factorplot(data=df, x="年报年份", y=variable_name, kind="swarm", hue=variable_name+"分布", size=6, aspect=2)
        return df
