#!/usr/bin/python
# coding: utf-8

import tushare as ts


class TuShare(object):
    def __init__(self, token):
        self.token = token
        self.pro = ts.pro_api(token, 2000)

    def get_stock_basic_info(self):
        data = self.pro.stock_basic(fields="ts_code,symbol,name,industry")
        return data.to_numpy()

    def get_stock_day_trade_info(self, code, start_date, end_date):
        data = self.pro.query('daily', ts_code=code, start_date=start_date, end_date=end_date)
        return data.to_numpy()



