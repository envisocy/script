import pandas as pd
import configure
import pymysql
import datetime
import numpy as np
import time


def request_df(sql_msg, date, variable="交易时间"):
    '''
    输出 df 表
    '''
    sql = "SELECT max(`" + variable + "`) FROM ERP_Sales_Ledger WHERE \
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
    sql_final = "SELECT `店铺`,`货品编号`,`数量`,`实际结算`,`交易时间`,`仓库` FROM \
    ERP_Sales_Ledger WHERE DATE_FORMAT(`" + variable +"`, '%Y-%m-%d')> '" +\
                datetime.datetime.strftime(date - datetime.timedelta(7),\
                                           "%Y-%m-%d") + "';"
                # *** Test 7->1->7
    df = pd.read_sql_query(sql_final, conn)
    conn.close()
    return df, date

def request_df_goodstable(sql_msg):
    conn = pymysql.connect(host=sql_msg["host"],
                          port=int(sql_msg["port"]),
                          user=sql_msg["user"],
                          passwd=sql_msg["passwd"],
                          charset=sql_msg["charset"],
                          db="baoersqlerp")
    sql = "SELECT * FROM ERP_Goods_Table;"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

class daily_report(object):
    def __init__(self, variable="交易时间", date=""):
        # 调用函数，读取 MySQL ERP 中的值
        print(" - 表单初始化中...")
        time_start=time.time()
        self._date = datetime.date.today() - datetime.timedelta(1) # datetime.date()
        self._sql = configure.echo("xiaobaods_r")["config"]
        self._df, self._date = request_df(self._sql, self._date, variable)
        # 添加日期列
        self._df["日期"] = self._df["交易时间"].map(lambda s:str(s).split()[0])
        # 提示表单上下限日期
        print(" - 表单准备完成，日期为：{} - {}，共 {} 行。".format(min(self._df[variable]),
                                    max(self._df[variable]), len(self._df)))
        # 格式化为 str的末日时间：
        self.date = datetime.datetime.strftime(self._date, "%Y-%m-%d")
        time_end=time.time()
        print(' - 表单准备耗时：{} s'.format(format(time_end-time_start, ".2f")))

    def company_sheet(self, variable="件数", origin=0):
        '''
        公司详情
        parameter:
        variable: 件数，销售额
        origin(Defalut=0): 输出表（0全表;1真实表;2补单表）
        '''
        if origin==1:
            df = self._df.loc[self._df["仓库"] != "虚拟仓库", :]
        elif origin==2:
            df = self._df.loc[self._df["仓库"] == "虚拟仓库", :]
        else:
            df = self._df
        variable_list = {"件数": "数量", "销售额": "实际结算", }
        df_company = pd.pivot_table(df, index="店铺", columns="日期", \
                                    values=(variable_list[variable]), \
                                    aggfunc=sum, fill_value=0)
        df_company.sort_values(df_company.columns[-1], ascending=False)
        df_company["week_mean"] = df_company.mean(axis=1)
        df_company["vs_mean"] = df_company.iloc[:,-3:-1].mean(axis=1)
        df_company.loc["total",:] = df_company.sum()
        # 替换日期
        df_company["week_ratio"] = df_company[self.date]/df_company["week_mean"]-1
        df_company["vs_ratio"] = df_company[self.date]/df_company["vs_mean"]-1
        return df_company.sort_values(self.date, ascending=False)

    def company_report(self, form="general"):
        '''
        Parameter：
        form:
        - general: 公司总况
            - 日期，week_mean, vs_mean, week_rotio, vs_ratio
            - 件数, 销售额
        - store: 销售直方图
            - 店铺, 件数, 销售额
            - total
        - percent: 比例图
            - percent, percent_week, percent_vs
        - sale_quote(origin): 销售指标
            - 日期, week_mean, vs_mean, week_ratio, vs_ratio
            - 店铺
        '''
        df1 = self.company_sheet( "件数")
        df2 = self.company_sheet( "销售额")
        if form == "general":
            df1.rename(index={"total": "件数"}, inplace=True)
            df2.rename(index={"total": "销售额"}, inplace=True)
            return pd.concat([df1.loc["件数", self.date:], \
                            df2.loc["销售额", self.date:]], axis=1).T
        if form == "store":
            df = pd.concat([df1[self.date], df2[self.date]], axis=1)
            df.columns = ["件数", "销售额"]
            return df.sort_values("件数", ascending=False)
        if form == "percent":
            df2["percent_vs"] = df2["vs_mean"]/df2.loc["total", "vs_mean"]
            df2["percent_week"] = df2["week_mean"]/df2.loc["total", "week_mean"]
            df2["percent"] = df2[self.date]/df2.loc["total", self.date]
            return df2.loc[:, ["percent", "percent_week", "percent_vs"]]
        if form == "sale_quote" or form == "origin":
            return df1
        return "No such Dataframe."

    def manul_operation(self, form="store"):
        '''
        Parameter：
        form:
        - general: 刷单原表
        - store: 店铺刷单表
        '''
        df_true = self.company_sheet(variable="件数", origin=1)
        df_manul = self.company_sheet(variable="件数", origin=2)
        df = pd.merge(df_true, df_manul, left_index=True, right_index=True, \
                      suffixes=('_true', '_manul'))
        if form == "general":
            return df
        if form == "store":
            df.rename(columns={self.date + "_true": "true", self.date + \
                               "_manul": "manul",}, inplace=True)
            df["manul_ratio"] = df["manul"]/df["true"]
            return df[["true", "manul", "manul_ratio"]]
        return "No such Dataframe."

    def type_sales_report(self, gt=0, num=0, instead=True, debug=False, origin=1):
        '''
        款式销售情况
        parameter
        gt: 总销量大于多少进行筛选
        num: 筛选出多少条数据(优先低于gt)
        默认：筛选出总条数的1/10的条目数
        instead(Default: True) 是否替换货号，默认替换
        debug(Default: False) 调试专用，输出筛选表、筛选行和筛选列
        origin(Default: 1) 是否包含补单数据，默认筛掉补单数据,0全表; 1真实值; 2补单数据
        '''
        df_goodstable = request_df_goodstable(sql_msg=self._sql)
        if origin==1:
            df = self._df.loc[self._df.loc[:, "仓库"] != "虚拟仓库", :]
            print("补单排除条目：{} / {} ( {} @ {} %)".format(len(df), \
                        len(self._df), len(self._df)-len(df), \
                        format(((1 - len(df) / len(self._df)) * 100), ".2f")))
        elif origin==2:
            df = self._df.loc[self._df.loc[:, "仓库"] == "虚拟仓库", :]
            print("补单排除条目：{} / {} ( {} @ {} %)".format(len(df), \
                        len(self._df), len(self._df)-len(df), \
                        format(((1 - len(df) / len(self._df)) * 100), ".2f")))
        else:
            df = self._df
            print("原始条目（含补单）：{}".format(len(df)))
        df.loc[df.loc[:, "数量"] > 5, "数量"] = 1
        df_sort =df.pivot_table(index="货品编号", columns="店铺", values="数量",
                                aggfunc="sum", fill_value=0)
        sort_columns = df_sort.sum(axis=0).sort_values(ascending=False).index.tolist()
        if gt:
            sort_index = df_sort.sum(axis=1).sort_values(ascending=False)[df_sort.sum(axis=1).values > gt].index.tolist()
        elif num:
            sort_index = df_sort.sum(axis=1).sort_values(ascending=False)[:num].index.tolist()
        else:
            sort_index = df_sort.sum(axis=1).sort_values(ascending=False)[:int(len(df_sort) / 10)].index.tolist()
        df_return = df.pivot_table(index="货品编号", columns="店铺", aggfunc="sum", values="数量", fill_value="")
        df_return = df_return.loc[sort_index, sort_columns]
        if instead:
            df_return.reset_index(inplace=True)
            df_return["条码"] = df_return["货品编号"].map(lambda s:df_goodstable.loc[s==df_goodstable["货品编号"], "条码"].values[0])
            df_return.set_index("条码", inplace=True)
            df_return.drop("货品编号", axis=1, inplace=True)
        if debug:
            return df_sort, sort_index, sort_columns
        return df_return

if __name__ == '__main__':
    d = daily_report()
    print(d.type_sales_report())
