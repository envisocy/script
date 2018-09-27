#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
__title__ = '生意参谋/市场/行业洞察 信息解析'
__author__ = 'Envisocy'
"""
import xiaobaods_input.Business_adviser_parser.get_page as get_page
import xiaobaods_input.Business_adviser_parser.parse_page as parse_page
import xiaobaods_input.Business_adviser_parser.save_data as save_data
import xiaobaods_input.Business_adviser_parser.detector as detector
from xiaobaods_input.Business_adviser_parser.config import *
VER = "Ver_11"
VER_DATE = "2018-07-20"


def main():
    htmls = get_page.from_desktop_text()
    table = ""
    for html in htmls:
        if html:
            print("###### Get html(", len(html), "Bytes ) ######")
            mode = parse_page.mode(html)
            if not mode:
                print("* 无法识别的项目类型！")
                continue
            msg = parse_page.parse_content(mode, html)
            msgt = parse_page.main_split(msg)  # 如果msg选择为时间段，则msgt返回为空
            if mode == 2:
                result = save_data.validation_exists2(msg["id"], msg["main"], sql_list=SQL_LIST)
                if result == 1:
                    continue
            save_data.prompt_message(mode, msg, detail=0)
            if not msgt:
                save_data.prompt_message(mode, msg, detail=1)
                print("* 选择日期为范围，无法解析数据内容！")
                continue
            else:
                msg = msgt
            if mode != 2:
                if validation_message(mode, msg):
                    save_data.prompt_message(mode, msg, detail=1)
                    continue
                items = parse_page.parse_main_control(mode, msg, html)
                table = save_data.save_main_control(mode, msg, items, sql_list=SQL_LIST, type="mysql")
            elif mode == 2:   # 2分四次传入
                items = parse_page.parse_page_mode2_0(msg, html)
                table = save_data.save_main_control(mode, msg, items, sql_list=SQL_LIST, type="mysql", table="bc_commodity_flow")
                items = parse_page.parse_page_mode2_1(msg, html)
                table = save_data.save_main_control(mode, msg, items, sql_list=SQL_LIST, type="mysql", table="bc_commodity_keywords")
                items = parse_page.parse_page_mode2_2(msg, html)
                table = save_data.save_main_control(mode, msg, items, sql_list=SQL_LIST, type="mysql", table="bc_commodity_association")
                items = parse_page.parse_page_mode2_3(msg, html)
                table = save_data.save_main_control(mode, msg, items, sql_list=SQL_LIST, type="mysql", table="bc_commodity_items")
                print("# Write Completion")
    input("### 录入完成！任意键输出结果检查...")
    detector.detector_main_control(mode=mode, table=table, sql_list=SQL_LIST, date=msg["main"])


def validation_message(mode, msg):
    # for mode 1,3&4
    if mode == 1 and msg.get('category') != "女装/女士精品":
        print("* 品类选择错误，请选择根目录，以免商品信息缺失！")
        return 1
    elif mode == 3 and msg.get('category') not in MODE3_PERMIT:
        print("* 品类选择超出范围，请确认或更改许可，以免商品信息混乱！")
        return 1
    elif mode == 4 and msg.get('category') not in MODE4_PERMIT:
        print("* 品类选择超出范围，请确认或更改许可，以免商品信息混乱！")
        return 1
    if mode == 4 and msg.get('attribute') not in MODE4_PERMIT[msg['category']]:
        print("* 品类选择超出限定范围，请确认或更改许可，以免商品信息混乱！")
        return 1
    if msg.get('device') != "所有终端":
        print("* 请选择终端为'所有终端'，以免信息缺失！")
        return 1
    if msg.get('seller') != "全网":
        print("* 请选择渠道为'全网'，以免信息缺失！")
        return 1
    if msg.get('quantity') != '100':
        print("* 请选择每页最大显示数为100，并重新处理该部分数据！")
        return 1
    return None


def main_detector():
    print("-" * 30)
    print(" # 请输入需检测的项目：")
    print(" 1. 商品店铺榜 -> 品牌粒度 -> 热销商品榜/流量商品榜")
    print(" 2. 商品店铺榜 -> 商品详情")
    print(" 0. 返回.")
    goto_detector()


def goto_detector():
    choice = input(" # 键入数字选择：")
    if choice == "0":
        main()
    elif choice == "1" or choice == "":
        mode = 1
        detector.detector_main_control(mode)
    elif choice == "2":
        mode = 2
        detector.detector_main_control(mode)
    else:
        print(" * 输入无效，请重新输入！")
        goto_detector()


if __name__ == '__main__':
    print("*" * 87)
    print("*" * 20, " Xiaobaods.com 生意参谋数据收集系统 ", VER, " ", "*" * 20)
    print("*" * 20, " - 宝儿电商 【数据组】  更新：", VER_DATE, " - ", "*" * 20)
    print(
        "*" * 87)
    main()
