#!/usr/bin/python
# coding: utf-8

from config import local
from util import date_util

import sys
import os
import django

# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sharewizard.settings")

django.setup()

from ashare.models import Company, Trade, Strategy

from ashare.strategy.Shrink import Shrink


def work():
    all_company = Company.objects.all()
    today = date_util.today()
    s_40_day_ago = date_util.get_n_days_ago(40)
    process = 0
    shrink_strategy = Shrink()
    for company in all_company:
        process += 1
        if process % 100 == 0:
            print(process)
        price_list = Trade.objects.order_by('-t_date').filter(company=company, t_date__gt=s_40_day_ago.strftime("%Y-%m-%d"),
                                                                 t_date__lt=today.strftime("%Y-%m-%d")).values_list('close', 'amount')
        if shrink_strategy.filter(price_list):
            print(company)


if __name__ == "__main__":
    work()