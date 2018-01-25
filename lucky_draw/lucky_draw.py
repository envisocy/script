#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
import random
import os
import sys

class lucky_draw:
    def __init__(self):
        # 奖项：[计划总人数, 已产生的人数, 每次输出人数, ]
        self.price_limit = {1: [10, 0, 2], 2: [20, 0, 5], 3: [30, 0, 10]}
        self.path = os.path.split(os.path.realpath(__file__))[0] + os.sep
        print ("\n")
        print ("*" * 12 , "宝儿电商年会抽奖程序", "*" * 12)
        self.init()

    def view(self):
        print("*" * 46)
        print(" * 成功找到共有{}人在抽奖池！".format(len(self.uplist)))
        print(" * 其中共有{}人拥有抽奖资格！（已中奖{}人！）".format(len(self.emplist), len(self.emplist) - len(self.uplist)))
        for i in range(3):
            print(" * 其中“{}等奖”已产生了 {} / {} 人".format(i+1, self.price_limit[i+1][1], self.price_limit[i+1][0]))
        print("*" * 46)

    def init(self):
        print (" * 载入全员名单，初始化中...")
        self.emplist = []
        self.uplist = []
        for i in range(3):
            self.price_limit[i+1][1] = 0
        with open(self.path + "List_table.csv", 'r', encoding='gbk') as f:
            empf = csv.reader(f)
            for emp in empf:
                self.emplist.append(emp)
                if emp[3] == "0":
                    self.uplist.append(emp)
                elif emp[3] in ["1", "2", "3"]:
                    self.price_limit[int(emp[3])][1] += 1
        self.view()

    def clear(self):
        for emp in range(len(self.emplist)):
            self.emplist[emp][3] = "0"
        with open(self.path + "List_table.csv", 'w', encoding='gbk') as f:
            for emp in self.emplist:
                f.write(",".join(emp)+"\n")
        print(" * 初始化所有{}人的抽奖资格完毕！".format(len(self.emplist)))
        self.init()

    def draw(self, price:int=0, num:int=0):
        price = int(price)
        if price not in [1, 2, 3]:
            print(" ! 无效的抽奖操作，未指定奖项！")
            return None
        if num == 0:
            num = self.price_limit[price][2]
        price_list = []
        if self.price_limit[price][1] + num > self.price_limit[price][0]:
            print(" ! 超出抽奖预计的人数")
        for i in range(num):
            # 产生中奖人
            price_name = random.choice(self.uplist)
            price_list.append(price_name)
            # 修改基础的中奖状态
            self.emplist[self.emplist.index(price_name)][3] = str(price)
            # 中奖列表中移除
            self.uplist.remove(price_name)
            print(" * {}等奖抽出：{}(第{}个)：".format(price, price_name[0], self.price_limit[price][1] + i + 1))
        with open(self.path + "List_table.csv", 'w', encoding='gbk') as f:
            for emp in self.emplist:
                f.write(",".join(emp)+"\n")
        self.price_limit[price][1] += num
        return price_list

    def result(self, price_target=0):
        if price_target == 0:
            price_range = [1, 2, 3]
        else:
            price_range = [price_target]
        price_list = {}
        for price in price_range:
            price_list[price] = []
            for emp in self.emplist:
                if emp[3] == str(price):
                    price_list[price].append(emp)
        print(price_list)
        return price_list

if __name__ == '__main__':
    try:
        argv = sys.argv[1]
        argv = str(argv)
    except:
        argv = "1"
    ld = lucky_draw()
    if argv in ["1", "2", "3"]:
        ld.draw(int(argv))
    elif argv == "c":
        ld.clear()
    elif argv == "v":
        ld.view()
    elif argv == "r":
        ld.result(0)
    elif argv in ["r0", "r1", "r2", "r3"]:
        ld.result(int(argv[1]))
