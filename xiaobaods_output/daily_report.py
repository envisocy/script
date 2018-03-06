import pandas as pd
import configure
import pymysql
import datetime
import numpy as np


def request_df(sql_msg, date, variable="交易时间"):
    '''
    输出 df 表
    '''
    sql = "SELECT max(`" + variable + "`) FROM ERP_Sales_ledger WHERE \
    DATE_FORMAT(`" + variable + "`, '%Y-%m-%d')='" +\
    datetime.datetime.strftime(date, "%Y-%m-%d") + "';"
    conn = pymysql.connect(host=sql_msg["host"],
                          port=int(sql_msg["port"]),
                          user=sql_msg["user"],
                          passwd=sql_msg["passwd"],
                          charset=sql_msg["charset"],
                          db="baoersqlerp")
    df_date = pd.read_sql_query(sql, conn)
    if not len(df_date):
        request_df(sql_msg, date-datetime.timedelta(1), variable)
    # 更新为7天数据
    sql_final = "SELECT * FROM ERP_Sales_ledger WHERE \
                DATE_FORMAT(`" + variable +"`, '%Y-%m-%d')> '" +\
                datetime.datetime.strftime(date - datetime.timedelta(7),
                                           "%Y-%m-%d") + "';"
    df = pd.read_sql_query(sql_final, conn)
    conn.close()
    return df, date

class daily_report(object):
    def __init__(self, variable="交易时间", date=""):
        # 调用函数，读取 MySQL ERP 中的值
        print(" - 表单初始化中...")
        self._date = datetime.date.today() - datetime.timedelta(1) # datetime.date()
        self._sql = configure.echo("xiaobaods_r")["config"]
        self._df, self._date = request_df(self._sql, self._date, variable)
        # 添加日期列
        self._df["日期"] = self._df["交易时间"].map(lambda s:str(s).split()[0])
        # 提示表单上下限日期
        print(" - 表单准备完成，日期为：{} - {}，共{}行。".format(min(self._df[variable]),
                                    max(self._df[variable]), len(self._df)))
        # 格式化为str的末日时间：
        self.date = datetime.datetime.strftime(self._date, "%Y-%m-%d")

    def company_sheet(self, variable="件数"):
        '''
        公司详情
        parameter:
        variable: 件数，销售额
        '''
        variable_list = {"件数": "数量", "销售额": "实际结算", }
        df_company = pd.pivot_table(self._df, index="店铺", columns="日期", \
                                    values=(variable_list[variable]), \
                                    aggfunc=sum, fill_value=0)
        df_company.sort_values(df_company.columns[-1], ascending=False)
        df_company["week_mean"] = df_company.mean(axis=1)
        df_company["vs_mean"] = df_company.iloc[:,-3:-1].mean(axis=1)
        df_company.loc["total",:] = df_company.sum()
        # 替换日期
        df_company["week_ratio"] = df_company[self.date]/df_company["week_mean"]-1
        df_company["vs_ratio"] = df_company[self.date]/df_company["vs_mean"]-1
        return df_company

    def company_report(self, form="general"):
        '''
        Parameter：
        form:
        - general: 公司总况
        - hist: 销售直方图
        '''
        df1 = company_sheet("件数")
        df2 = company_sheet("销售额")
        if form == "general":
            df1.rename(index={"total": "件数"}, inplace=True)
            df2.rename(index={"total": "销售额"}, inplace=True)
            '''
            日期, 2018-03-05, week_mean, vs_mean, week_ratio, vs_ratio
            件数  xxx, xxx, xxx, xxx, xxx
            销售额 xxxxx, xxxxx, xxxxx, xxxxx, xxxxx
            '''
            return pd.concat([df1.loc["件数", self.date:], \
                            df2.loc["销售额", self.date:]], axis=1).T
        if form == "hist":
            df = pd.concat([df1["2018-03-05"], df2["2018-03-05"]], axis=1)
            '''
            店铺, 件数, 销售额
            ...
            total xxx, xxxxx
            '''
            df.columns = ["件数", "销售额"]
            return df
        if form == "percent":
            df2["percent_vs"] = df2["vs_mean"]/df2.loc["total", "vs_mean"]
            df2["percent_week"] = df2["week_mean"]/df2.loc["total", "week_mean"]
            df2["percent"] = df2[self.date]/df2.loc["total", self.date]
            '''
            percent, percent_week, percent_vs
            ... xxx, xxx, xxx
            '''
            return df2.loc[:, ["percent", "percent_week", "percent_vs"]]


    def manul_operation(self):
        '''
        刷单表
        '''
        pass

    def store_sales_report(self):
        '''
        店铺销售情况
        '''
        pass

    def type_sales_report(self):
        '''
        款式销售情况
        '''
        pass