
department_table = {"customer_service": "customer_service",
                    }

'''
index: "表名_table"#"职位_position"
    - type
        - "value": 直接传入值；
        - "multiplier": 通过数据直接传入值；variable
        - "rank": 通过数据排名值换算；
        - "range/percentage": 通过数据值范围换算 , 百分比解析时会乘100；
        - "times": 通过数据值范围换算；
'''

# alias 别名 date 日期

kpi_index_default = {"customer_service#售前":
    {1: {"weight": 10, "name": "销售量排名", "variable": "销售量排名", "type": "rank", "goal":
        {"-3:": 0,"11:-4": 0.6, "6:10": 0.8, "2:5": 1, "1": 1.2, "D1": 1.5}},
    2: {"weight": 15, "name": "询单转化率", "variable": "转化率", "type": "percentage", "goal":
        {":45": 0, "45: 50": 0.6, "50: 55": 0.8, "55: 56": 1, "56:62": 1.2, "62:": 1.5}},
    3: {"weight": 15, "name": "退款率", "variable": "退款率", "type": "percentage", "goal":
        {"21:": 0, "16: 21": 0.6, "13: 16": 0.8, "12: 13": 1, "10: 12": 1.2, ":10": 1.5}},
    4: {"weight": 10, "name": "旺旺接待答问比", "variable": "答问比", "type": "percentage", "goal":
        {":100": 0, "100: 120": 0.6, "120: 130": 0.8, "130: 200": 1, "200: 300": 1.2, "300:": 1.5}},
    5: {"weight": 10, "name": "平均响应时间", "variable": "响应时间", "type": "range", "goal":
        {"40:": 0, "35: 40": 0.6, "28: 35": 0.8, "25: 28": 1, "18: 25": 1.2, ":18": 1.5}},
    6: {"weight": 10, "name": "客户满意度发送率", "variable": "发送率", "type": "percentage", "goal":
        {":60": 0, "60: 65": 0.6, "65: 70": 0.8, "70: 75": 1, "75: 90": 1.2, "90:": 1.5}},
    7: {"weight": 10, "name": "公司所有店铺目标达成率", "variable": "公司店铺目标达成率", "type": "value", "goal":
        1, "reach": "0.92", "extent": "0.9+"},
    8: {"weight": 20, "name": "工作能力考核", "variable": "工作能力考核", "type": "multiplier"},},
}
