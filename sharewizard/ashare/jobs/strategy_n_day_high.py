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

from ashare.models import Company, Trade, Strategy, Industry

from ashare.strategy.NDayHigh import NDayHigh


def work(begin_date, end_date):
    all_company = Company.objects.all()
    n_day_high = NDayHigh()
    process = 0
    s_15_day_high_company = []
    s_30_day_high_company = []
    s_60_day_high_company = []
    s_120_day_high_company = []
    for company in all_company:
        process += 1
        if process % 100 == 0:
            print(process)
        price_list = Trade.objects.order_by('-t_date').filter(company=company, t_date__gt=begin_date.strftime("%Y-%m-%d"),
                                                                 t_date__lt=end_date.strftime("%Y-%m-%d")).values_list('close')

        # company_trade_info = []
        # for company_trade_item in company_trade.objects.all():
        #     company_trade_info.append(company_trade_item)

        # price_list = [trade_info.close for trade_info in company_trade_info]

        if n_day_high.is_15_day_high(price_list):
            strategy = Strategy(t_date=end_date, company=company, t_type=Strategy.T_15_DAYS)
            strategy.save()

            s_15_day_high_company.append(company)

        if n_day_high.is_30_day_high(price_list):
            strategy = Strategy(t_date=end_date, company=company, t_type=Strategy.T_30_DAYS)
            strategy.save()

            s_30_day_high_company.append(company)

        if n_day_high.is_60_day_high(price_list):
            strategy = Strategy(t_date=end_date, company=company, t_type=Strategy.T_60_DAYS)
            strategy.save()

            s_60_day_high_company.append(company)

        if n_day_high.is_120_day_high(price_list):
            strategy = Strategy(t_date=end_date, company=company, t_type=Strategy.T_120_DAYS)
            strategy.save()

            s_120_day_high_company.append(company)

    industry_count(end_date, s_15_day_high_company, Industry.T_15_DAYS)
    industry_count(end_date, s_30_day_high_company, Industry.T_30_DAYS)
    industry_count(end_date, s_60_day_high_company, Industry.T_60_DAYS)
    industry_count(end_date, s_120_day_high_company, Industry.T_120_DAYS)


def industry_count(cur_date, company_list, strategy_type):
    industry_high_count = {}
    for company in company_list:
        industry_high_count[company.industry] = industry_high_count.get(company.industry, 0) + 1

    for industry, count in industry_high_count.items():
        print(industry, count)
        industry_model = Industry(t_date=cur_date, name=industry, t_type=strategy_type, number=count)
        industry_model.save()


if __name__ == "__main__":
    for i in range(0, 1):
        end_date = date_util.get_n_days_ago(i)
        begin_date = date_util.get_n_days_ago(180+i)
        work(begin_date, end_date)
