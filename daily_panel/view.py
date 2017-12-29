#!usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import time
import numpy as np


class dashboard():
    def __init__(self, argv=0, sleep=30):
        self.argv = argv
        self.sleep = sleep

    def get_information(self):
        text = "Panel - " + time.strftime("%I:%M:%S %p   %Z", time.localtime()) + \
        ",   Sleep " + str(self.sleep) + "s, " +\
         time.strftime("   Week: %W,   %A %B %d", time.localtime()) + "\n"
        text += "(EST) - " + time.strftime("%I:%M:%S %p", time.localtime(time.time() - 57600)) + \
        "   (WST) - " + time.strftime("%I:%M:%S %p", time.localtime(time.time() - 46800)) + \
        "   (Seoul) - " + time.strftime("%I:%M:%S %p", time.localtime(time.time() + 3600)) +"\n"
        if self.argv == 0:
            text += "Tasks1: "
            text += self.coin()
        return text

    def view(self, text=""):
        if "win" in sys.platform:
            os.system("cls")
        elif "linux" in sys.platform:
            os.system("clear")
        print(text)

    def run(self):
        while True:
            self.view(self.get_information())
            time.sleep(self.sleep + np.random.random_sample()*self.sleep/5)

    def coin(self):
        from coinmarketcap import Market
        coinmarketcap = Market()
        text = time.strftime("%I:%M:%S %p", \
            time.localtime(int(coinmarketcap.ticker('bitcoin', convert="CNY")\
                               [0]['last_updated']))) + " updated\n\n"
        text += "\033[7;37;40mSym     Rank       %Cper           Prc        \
            Changes       \033[0m \n"
        for c in ['bitcoin', 'ethereum', 'ripple', 'bitcoin-cash', 'litecoin',
                  'EOS', 'bitcoin-gold', 'qtum', 'bitshares', 'binance-coin',
                  'digixdao', 'gxshares', 'decentraland']:
            msg = coinmarketcap.ticker(c, convert="CNY")[0]
            text += msg["symbol"].lower() + "\t" + msg["rank"] + "\t" + \
            str("%.8f"%float(msg["price_btc"])) + "\t" + \
            " " * (8-len(str("%.2f"%float(msg["price_cny"])))) + \
            str("%.2f"%float(msg["price_cny"])) + "\t" + \
            " " * (7-len(str("%.2f"%float(msg['percent_change_1h'])))) + \
             str("%.2f"%float(msg['percent_change_1h'])) + " /" +\
            " " * (7-len(str("%.2f"%float(msg['percent_change_24h'])))) + \
             str("%.2f"%float(msg['percent_change_24h'])) + " /" +\
            " " * (7-len(str("%.2f"%float(msg['percent_change_7d'])))) + \
             str("%.2f"%float(msg['percent_change_7d'])) + "\n"
        return text
