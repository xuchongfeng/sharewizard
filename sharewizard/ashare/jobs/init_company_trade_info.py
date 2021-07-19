#!/usr/bin/python
# coding: utf-8

from service.tu_share import TuShare

import sys
import os
import django

# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharewizard.settings")

django.setup()

from ashare.models import Company, Trade

TOKEN = "53d33fa381e94af6cd8e5b5165d5802ad40dd92a5094a6dd175d2a89"


def work():
    tu_share = TuShare(TOKEN)
    stock_list = tu_share.get_stock_basic_info()
    idx = 0
    for stock in stock_list:
        print(idx)
        idx += 1
        code, name = stock[0], stock[2]
        stock_trade_info = tu_share.get_stock_day_trade_info(code, "20210714", "20210716")
        try:
            company = Company.objects.filter(code=code)[0]
        except Exception:
            print(company)
            continue
        for stock_trade in stock_trade_info:
            t_date, open, high, low, close, amount, value = stock_trade[1], stock_trade[2], stock_trade[3], \
                                                            stock_trade[4], stock_trade[5], stock_trade[9], stock_trade[
                                                                10]
            try:
                trade_model = Trade(company=company,
                                    t_date=t_date[0:4]+"-"+t_date[4:6]+"-"+t_date[6:8],
                                    high=high * 100,
                                    low=low * 100,
                                    close=close * 100,
                                    open=open * 100,
                                    amount=amount * 100,
                                    value=value * 100)
                trade_model.save()
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    work()
